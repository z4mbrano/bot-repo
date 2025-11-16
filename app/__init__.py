from flask import Flask
from flask_cors import CORS

def create_app():
    """Fábrica de Aplicação (Application Factory)"""
    
    app = Flask(__name__)
    
    # Habilita CORS (ainda é útil para testar direto do seu frontend)
    CORS(app) 

    # Importa e registra as rotas (endpoints)
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    print("🚀 Aplicação Flask (IA) criada e rotas registradas.")
    return app