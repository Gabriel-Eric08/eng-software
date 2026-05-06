# Ruralize - Plataforma de Impacto Social UFRPE

Projeto de Engenharia de Software - Sistema de gamificação para horas de extensão universitária.

## 🚀 Funcionalidades

✅ **Sistema de Autenticação Completa**
- Cadastro de usuário com nome, email, telefone e senha
- Login com email e senha
- Senhas criptografadas com bcrypt
- Sessão de usuário persistente

✅ **Perfil de Usuário Dinâmico**
- Nível e sistema de XP
- Horas contribuídas
- Contagem de ações validadas
- Progresso de nível em tempo real
- Histórico completo de atividades

✅ **Arquitetura em Camadas**
```
📁 app.py               -> Aplicação principal Flask
📁 services/            -> Camada de negócio
   ↳ usuario_service.py
📁 routes/              -> Camada API REST
   ↳ usuario_routes.py
📁 templates/           -> Camada Frontend
   ↳ index.html
```

✅ **Banco de Dados SQLite**
- Tabela `usuarios` com todos os dados de perfil
- Tabela `atividades` com histórico de ações
- Relacionamento 1:N entre usuário e atividades

## 🔧 Instalação e Execução

1. Instale as dependências:
```bash
pip install flask bcrypt
```

2. Execute a aplicação:
```bash
python3 app.py
```

3. Acesse no navegador:
```
http://127.0.0.1:5000
```

## 🔑 Usuário Padrão

```
Email: roberto@ufrpe.br
Senha: 123456
```

## 📡 API Endpoints

| Método | Rota                   | Descrição
|--------|------------------------|--------------------------------
| POST   | `/api/usuario/cadastro`| Cadastra novo usuário
| POST   | `/api/usuario/login`   | Autentica usuário
| POST   | `/api/usuario/logout`  | Finaliza sessão
| GET    | `/api/usuario/me`      | Retorna dados do usuário logado

## 🎨 Interface

- Design institucional seguindo manual de marca UFRPE
- Cores oficiais: Azul Marinho `#1E2B4F` e Dourado `#F9B233`
- Responsivo para mobile
- Modal de login/cadastro moderno
- Animações e transições suaves

## 🛠 Tecnologias

✅ **Backend:** Python + Flask
✅ **Banco:** SQLite 3
✅ **Frontend:** HTML5 + Tailwind CSS
✅ **Autenticação:** bcrypt + Flask Session
✅ **API:** REST JSON

## ✅ Status do Projeto

✅ Funcionalidades básicas implementadas
✅ Autenticação funcionando
✅ Dados dinâmicos do banco
✅ Interface finalizada
✅ Testes realizados