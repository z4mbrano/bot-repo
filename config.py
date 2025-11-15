"""
Configurações centralizadas do projeto Cloud Solution Advisor
"""

import os

# URLs da API (override via env vars in production)
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:5000")
API_CHAT_URL = f"{API_BASE_URL}/api/chat"
API_TEST_URL = f"{API_BASE_URL}/api/test"
API_HISTORY_URL = f"{API_BASE_URL}/api/history"

# Configurações do Google AI (use variáveis de ambiente)
# IMPORTANT: Do NOT commit real API keys to source control. Set them in the host environment.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyC5qEJ7TBSxndhoB3ZzogVxAbiCkqKg8TU")
GOOGLE_AI_MODEL = os.environ.get("GOOGLE_AI_MODEL", "gemini-2.5-flash")

# Configurações dos Bots
BOT_TYPES = {
    "querrybot": "Oracle QueryBot - Especialista em soluções Oracle Cloud",
    "querryarc": "Oracle QueryArc - Arquiteto de soluções Oracle Cloud"
}

# Configurações de desenvolvimento (override with env vars in deploy)
DEBUG_MODE = os.environ.get("DEBUG_MODE", "True").lower() in ("1", "true", "yes")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
try:
    BACKEND_PORT = int(os.environ.get("BACKEND_PORT", "5000"))
except Exception:
    BACKEND_PORT = 5000