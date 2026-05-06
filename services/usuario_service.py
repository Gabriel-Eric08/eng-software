import sqlite3
import bcrypt

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_usuario_by_id(usuario_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    conn.close()
    
    if usuario is None:
        return None
    
    usuario = dict(usuario)
    # Não retorna a senha
    usuario.pop('senha', None)
    return usuario

def get_usuario_by_email(email):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if usuario is None:
        return None
        
    return dict(usuario)

def criar_usuario(nome, email, telefone, senha):
    conn = get_db_connection()
    
    # CORREÇÃO: Lógica mais segura para iniciais
    partes_nome = nome.strip().upper().split()
    if len(partes_nome) > 1:
        iniciais = partes_nome[0][0] + partes_nome[-1][0]
    elif len(partes_nome) == 1:
        # Se digitar só um nome, pega as duas primeiras letras (ou uma se só tiver uma)
        iniciais = partes_nome[0][:2] 
    else:
        iniciais = "XX" # Fallback se vier vazio
    
    # CORREÇÃO: Decode para string antes de salvar no banco
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
    
    try:
        cursor = conn.execute('''
        INSERT INTO usuarios (nome, email, telefone, senha, iniciais)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, telefone, senha_hash, iniciais))
        
        conn.commit()
        usuario_id = cursor.lastrowid
        conn.close()
        
        return get_usuario_by_id(usuario_id)
    except sqlite3.IntegrityError:
        conn.close()
        # Aqui é onde seu 409 nasce! Isso significa que o e-mail já está no banco.
        return None

def verificar_login(email, senha):
    usuario = get_usuario_by_email(email)
    
    if not usuario:
        return None
        
    # CORREÇÃO: Codifica a senha do banco de volta para bytes para o checkpw
    if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
        usuario.pop('senha', None)
        return usuario
    
    return None

def get_atividades_usuario(usuario_id):
    conn = get_db_connection()
    atividades = conn.execute('SELECT * FROM atividades WHERE usuario_id = ? ORDER BY data DESC', (usuario_id,)).fetchall()
    conn.close()
    
    return [dict(atividade) for atividade in atividades]

def get_dados_completos_usuario(usuario_id):
    usuario = get_usuario_by_id(usuario_id)
    
    if not usuario:
        return None
        
    atividades = get_atividades_usuario(usuario_id)
    
    return {
        **usuario,
        'atividades': atividades
    }
