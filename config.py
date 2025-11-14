"""
Configurações centralizadas do projeto Cloud Solution Advisor
"""

# URLs da API
API_BASE_URL = "http://127.0.0.1:5000"
API_CHAT_URL = f"{API_BASE_URL}/api/chat"
API_TEST_URL = f"{API_BASE_URL}/api/test"
API_HISTORY_URL = f"{API_BASE_URL}/api/history"

# Configurações do Google AI
GOOGLE_API_KEY = "AIzaSyC5qEJ7TBSxndhoB3ZzogVxAbiCkqKg8TU"
GOOGLE_AI_MODEL = "gemini-2.5-flash"

# Configurações dos Bots
BOT_TYPES = {
    "querrybot": "Oracle QueryBot - Especialista em soluções Oracle Cloud",
    "querryarc": "Oracle QueryArc - Arquiteto de soluções Oracle Cloud"
}

# Configurações de desenvolvimento
DEBUG_MODE = True
FRONTEND_URL = "http://localhost:5173"
BACKEND_PORT = 5000