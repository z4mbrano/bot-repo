import google.generativeai as genai

# Configurar com a chave
GOOGLE_API_KEY = "AIzaSyC5qEJ7TBSxndhoB3ZzogVxAbiCkqKg8TU"

try:
    print("🧪 Testando Google AI diretamente...")
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Criar modelo - usar o mesmo modelo da API
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Teste simples
    response = model.generate_content("Diga olá em português")
    
    print(f"✅ Sucesso! Resposta: {response.text}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    print(f"Stack trace: {traceback.format_exc()}")