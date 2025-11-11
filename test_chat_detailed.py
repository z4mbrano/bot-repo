import requests
import json
import time

def test_chat():
    try:
        print("🧪 Testando chat do bot...")
        
        data = {
            'message': 'Minha empresa tem um e-commerce antigo em um servidor monolítico. É lento e cai toda Black Friday. Quero modernizar tudo para uma arquitetura de microsserviços que seja escalável e resiliente na nuvem.',
            'bot_id': 'querryarc',
            'chat_id': f'test_{int(time.time())}'
        }
        
        print(f"Enviando para: http://localhost:5000/api/chat")
        print(f"Dados: {json.dumps(data, indent=2)}")
        
        response = requests.post('http://localhost:5000/api/chat', json=data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"\n✅ Sucesso!")
            print(f"Bot: {response_data.get('bot_name')}")
            print(f"Mensagem: {response_data.get('message')}")
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_chat()