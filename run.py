from app import create_app
from config import PORT, DEBUG_MODE

# Cria a aplicação usando a fábrica
app = create_app()

if __name__ == '__main__':
    print(f"🚀 Iniciando servidor de IA (Python) em http://0.0.0.0:{PORT}")
    print(f"🔧 Modo debug: {DEBUG_MODE}")
    app.run(debug=DEBUG_MODE, port=PORT, host='0.0.0.0')