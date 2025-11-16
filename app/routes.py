from flask import Blueprint, request, jsonify
from app.ai_service import generate_ai_response
from config import DEBUG_MODE, GOOGLE_API_KEY

# Cria um "Blueprint", que é um conjunto de rotas
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint principal de chat. Não salva histórico.
    Recebe: { "message": "...", "bot_id": "...", "history": [...] }
    Retorna: { "message": "..." }
    """
    try:
        data = request.json
        print(f"Dados recebidos na rota: {data.get('bot_id')}, {len(data.get('message', ''))} chars")

        user_message = data.get('message')
        bot_id = data.get('bot_id')
        history = data.get('history', []) # Recebe o histórico do Java

        if not user_message or not bot_id:
            return jsonify({'error': 'Os campos "message" e "bot_id" são obrigatórios'}), 400

        # Chama o serviço de IA (separado)
        bot_response = generate_ai_response(user_message, bot_id, history)
        
        # O Java só precisa do campo 'message'
        return jsonify({
            'message': bot_response
        })

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
        return jsonify({'error': str(ve)}), 400 # Ex: Bot não encontrado
    except Exception as e:
        print(f"Erro inesperado na rota /api/chat: {e}")
        return jsonify({
            'error': 'Erro interno do servidor de IA',
            'details': str(e) if DEBUG_MODE else None
        }), 500

@api_bp.route('/api/test', methods=['GET'])
def test():
    """Endpoint de teste para verificar se a API está no ar."""
    return jsonify({
        'status': 'Serviço de IA (Python) está funcionando',
        'google_api_configured': GOOGLE_API_KEY is not None
    })