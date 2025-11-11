from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'API funcionando', 'message': 'Teste simples'})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        print("=== Requisição recebida ===")
        data = request.json
        print(f"Dados: {data}")
        
        user_message = data.get('message', '')
        bot_id = data.get('bot_id', 'querrybot')
        
        print(f"Mensagem: {user_message}")
        print(f"Bot: {bot_id}")
        
        # Resposta simples para teste
        if bot_id == 'querryarc':
            bot_response = """Nome do Serviço: Oracle Container Engine for Kubernetes (OKE)
Categoria: Compute/Container
Justificativa Técnica: OKE oferece orquestração nativa de microsserviços com Kubernetes gerenciado, permitindo escalabilidade automática e alta disponibilidade para arquiteturas modernas de e-commerce.
Aspectos de Implementação: 
- Configure clusters OKE com auto-scaling para lidar com picos de Black Friday
- Implemente service mesh com Istio para comunicação segura entre microsserviços  
- Use Oracle Autonomous Database como backend para persistência de dados escalável"""
        else:
            bot_response = """Nome do Serviço: Oracle Autonomous Database
Categoria: Database
Justificativa Técnica: Banco de dados autogerenciado com escalabilidade automática, ideal para cargas de trabalho variáveis de e-commerce.
Argumentos de Venda: 
- Redução de 90% nos custos operacionais com automação completa
- Performance até 10x superior com otimização automática por IA
- Zero downtime com patches e upgrades automáticos"""
        
        print(f"Resposta gerada: {bot_response[:100]}...")
        
        return jsonify({
            'message': bot_response,
            'bot_name': f'Oracle Query{bot_id.title()}',
            'chat_id': data.get('chat_id', 'default'),
            'bot_id': bot_id
        })
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando API simplificada...")
    app.run(debug=True, port=5000)