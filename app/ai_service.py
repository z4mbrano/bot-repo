import google.generativeai as genai
import re
from app.prompts import bot_configs
from config import GOOGLE_API_KEY, GOOGLE_AI_MODEL

# Configurar o Google AI (só precisa ser feito uma vez)
try:
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("✅ Google AI (ai_service) configurado com sucesso")
    else:
        print("❌ GOOGLE_API_KEY não configurada (ai_service)")
except Exception as e:
    print(f"❌ Erro ao configurar API (ai_service): {e}")


def generate_ai_response(message: str, bot_id: str, history: list) -> str:
    """
    Gera uma resposta de IA usando o Google AI, com base no histórico enviado.
    """
    if bot_id not in bot_configs:
        raise ValueError(f"Bot ID '{bot_id}' não encontrado.")

    bot_config = bot_configs[bot_id]

    try:
        print(f"=== PROCESSANDO MENSAGEM COM IA (Bot: {bot_id}) ===")
        model = genai.GenerativeModel(GOOGLE_AI_MODEL)

        # 1. Construir o contexto a partir do histórico enviado pelo Java
        chat_context = ""
        if history:
            print(f"Incluindo contexto de {len(history)} mensagens anteriores")
            for msg in history:
                
                chat_context += f"{msg.get('role')}: {msg.get('message')}\n"
            
            chat_context += "\n"
        
        full_prompt = f"""INSTRUÇÕES: {bot_config['instructions']}

{chat_context}Usuário: {message}

Assistente:"""

        print(f"Enviando prompt para IA...")
        response = model.generate_content(full_prompt)
        
        if not response or not response.text:
            raise Exception("Resposta vazia da IA")

        bot_response = response.text.strip()
        print(f"✅ Resposta recebida: {len(bot_response)} caracteres")

        # 3. Formatar a resposta
        return _format_urls_as_markdown(bot_response)

    except Exception as ai_error:
        print(f"❌ ERRO DETALHADO na API do Google AI:")
        print(f"   Tipo do erro: {type(ai_error).__name__}")
        print(f"   Mensagem: {str(ai_error)}")
        # Retorna uma mensagem de fallback
        return f"Desculpe, estou com dificuldades técnicas. Como {bot_config['name']}, poderei ajudá-lo em breve."


def _format_urls_as_markdown(text: str) -> str:
    """Helper para formatar URLs em markdown."""
    # Detecta URLs que não estão em markdown
    url_pattern = r'(?<!\]\()(?<![\[\(])(https?://[^\s\)]+)'
    def replace_url(match):
        url = match.group(1)
        url = url.rstrip('.,;:!?"\'')
        return f'[{url}]({url})'
    
    result = re.sub(url_pattern, replace_url, text)
    # Corrige links markdown sem fechamento de parêntese
    result = re.sub(r'(\[https?://[^\]]+\]\(https?://[^\)\s]+)(?!\))', r'\1)', result)
    return result