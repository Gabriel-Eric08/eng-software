from flask import Flask, render_template, jsonify, request, session
from init_db import init_db
import os
from routes.usuario_routes import usuario_bp

app = Flask(__name__)
app.secret_key = 'ruralize_ufrpe_secret_key_2026_v2'

os.makedirs('models', exist_ok=True)
os.makedirs('services', exist_ok=True)
os.makedirs('routes', exist_ok=True)

app.register_blueprint(usuario_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)