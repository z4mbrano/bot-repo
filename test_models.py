import google.generativeai as genai

# Configurar com a chave
GOOGLE_API_KEY = "AIzaSyC5qEJ7TBSxndhoB3ZzogVxAbiCkqKg8TU"

try:
    print("🧪 Listando modelos disponíveis...")
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Listar modelos disponíveis
    models = genai.list_models()
    
    print("📋 Modelos disponíveis:")
    for model in models:
        print(f"   - {model.name}")
        
    # Testar com modelo correto
    print("\n🧪 Testando com modelo gemini-pro...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Diga olá em português")
    print(f"✅ Sucesso! Resposta: {response.text}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    print(f"Stack trace: {traceback.format_exc()}")