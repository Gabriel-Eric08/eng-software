from flask import Blueprint, jsonify, request, session
from services.usuario_service import get_dados_completos_usuario, criar_usuario, verificar_login

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuario/cadastro', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    
    if not all(k in dados for k in ['nome', 'email', 'senha']):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    usuario = criar_usuario(
        dados['nome'],
        dados['email'],
        dados.get('telefone'),
        dados['senha']
    )
    
    if not usuario:
        return jsonify({'erro': 'Email já cadastrado'}), 409
    
    session['usuario_id'] = usuario['id']
    return jsonify(usuario), 201

@usuario_bp.route('/usuario/login', methods=['POST'])
def login_usuario():
    dados = request.get_json()
    
    if not all(k in dados for k in ['email', 'senha']):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    usuario = verificar_login(dados['email'], dados['senha'])
    
    if not usuario:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401
    
    session['usuario_id'] = usuario['id']
    return jsonify(usuario)

@usuario_bp.route('/usuario/logout', methods=['POST'])
def logout_usuario():
    session.pop('usuario_id', None)
    return jsonify({'sucesso': True})

@usuario_bp.route('/usuario/me', methods=['GET'])
def obter_usuario_logado():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    dados = get_dados_completos_usuario(session['usuario_id'])
    
    if not dados:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
        
    return jsonify(dados)
