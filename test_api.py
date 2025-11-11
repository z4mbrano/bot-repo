import requests
import json

try:
    print("🧪 Testando API...")
    
    # Teste 1: Endpoint de teste
    print("\n1. Testando endpoint /api/test")
    response = requests.get('http://localhost:5000/api/test')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Teste 2: Chat
    print("\n2. Testando endpoint /api/chat")
    data = {
        'message': 'Preciso de um banco de dados para e-commerce',
        'bot_id': 'querrybot',
        'chat_id': 'test123'
    }
    response = requests.post('http://localhost:5000/api/chat', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Erro: {e}")