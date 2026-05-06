from flask import Flask, render_template, jsonify, request, session
import sqlite3
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'ruralize_ufrpe_secret_key_2026_v2'

# Cria as pastas se não existir
os.makedirs('models', exist_ok=True)
os.makedirs('services', exist_ok=True)
os.makedirs('routes', exist_ok=True)

# Inicializa banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT,
        senha TEXT NOT NULL,
        iniciais TEXT NOT NULL,
        nivel INTEGER NOT NULL DEFAULT 1,
        xp_atual INTEGER NOT NULL DEFAULT 0,
        xp_proximo_nivel INTEGER NOT NULL DEFAULT 500,
        horas_contribuidas INTEGER NOT NULL DEFAULT 0,
        acoes_validadas INTEGER NOT NULL DEFAULT 0,
        patente TEXT NOT NULL DEFAULT 'Membro Ruralize Bronze'
    )
    ''')
    
    # Tabela de Atividades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        data TEXT NOT NULL,
        local TEXT NOT NULL,
        xp INTEGER NOT NULL,
        horas INTEGER NOT NULL,
        icone TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    ''')
    
    # Insere usuário padrão Roberto Carlos se não existir
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    if cursor.fetchone()[0] == 0:
        
        # GERA O HASH DA SENHA "123" AQUI
        salt = bcrypt.gensalt()
        senha_hash_123 = bcrypt.hashpw('123'.encode('utf-8'), salt).decode('utf-8')
        
        cursor.execute('''
        INSERT INTO usuarios (nome, email, telefone, senha, iniciais, nivel, xp_atual, xp_proximo_nivel, horas_contribuidas, acoes_validadas, patente)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('Roberto Carlos', 'roberto@ufrpe.br', '81999999999', senha_hash_123, 'RC', 3, 350, 500, 12, 3, 'Membro Ruralize Bronze'))
        
        usuario_id = cursor.lastrowid
        
        # Insere atividades exemplo
        atividades = [
            (usuario_id, 'Monitoria de Matemática - Comunidade', '04 Mai 2024', 'Dois Irmãos', 80, 4, '📚'),
            (usuario_id, 'Reflorestamento Campus UFRPE', '28 Abr 2024', 'Campus Dois Irmãos', 120, 6, '🌱'),
            (usuario_id, 'Apoio Digital Idosos Ipsep', '15 Abr 2024', 'Ipsep', 100, 5, '💻')
        ]
        
        cursor.executemany('''
        INSERT INTO atividades (usuario_id, titulo, data, local, xp, horas, icone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', atividades)
    
    conn.commit()
    conn.close()

# Importa e registra rotas
from routes.usuario_routes import usuario_bp
app.register_blueprint(usuario_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)