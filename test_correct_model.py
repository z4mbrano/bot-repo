import google.generativeai as genai

# Configurar com a chave
GOOGLE_API_KEY = "AIzaSyC5qEJ7TBSxndhoB3ZzogVxAbiCkqKg8TU"

try:
    print("🧪 Testando com modelo gemini-2.0-flash-exp...")
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Testar com modelo correto
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Diga olá em português")
    print(f"✅ Sucesso! Resposta: {response.text}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    print(f"Stack trace: {traceback.format_exc()}")