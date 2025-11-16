import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Configurações da IA ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_AI_MODEL = os.environ.get("GOOGLE_AI_MODEL", "gemini-1.5-flash")

# --- Configurações do Servidor ---
PORT = int(os.environ.get("AI_SERVICE_PORT", 5001))
DEBUG_MODE = os.environ.get("FLASK_DEBUG", "True").lower() == "true"