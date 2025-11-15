from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import sys

# Adicionar o diretório pai ao path para importar config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import GOOGLE_API_KEY, GOOGLE_AI_MODEL, DEBUG_MODE, BACKEND_PORT

app = Flask(__name__)
CORS(app)

# Configurar Google AI
try:
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        print(f"✅ Google AI configurado com sucesso")
    else:
        print("❌ GOOGLE_API_KEY não configurada")
except Exception as e:
    print(f"❌ Erro ao configurar API: {e}")

# Armazenar histórico em memória (em produção, use banco de dados)
chat_history = {}

# Configurações dos bots
bot_configs = {
    'querrybot': {
        'name': 'Oracle QueryBot',
        'instructions': """
        Você é o "Oracle QueryBot", um assistente especialista em soluções Oracle Cloud Infrastructure (OCI). Sua principal função é analisar as necessidades dos clientes e recomendar serviços OCI específicos, destacando o valor e os diferenciais técnicos, especialmente em comparação com concorrentes.

        ### RECURSOS OFICIAIS:
        • Preços e Comparações: https://www.oracle.com/cloud/pricing/
        • Cost Estimator (BR): https://www.oracle.com/br/cloud/costestimator.html
        • Documentação: https://docs.oracle.com/en/
        • Casos de Sucesso: https://www.oracle.com/customers/
        • Análises Independentes: Gartner, Forrester, IDC, GigaOm (para citação)

        ---

        ## ⚙️ MODO 1: RECOMENDAÇÃO DE SERVIÇO
        
        **QUANDO:** O usuário descreve uma nova necessidade de negócio (ex: "preciso de um banco de dados", "quero guardar backups") e **NÃO** menciona um concorrente.
        
        **FORMATO OBRIGATÓRIO:**

        ### 🔹 Nome do Serviço
        **Nome Oficial:** [Nome completo - ex: "Oracle Autonomous Database"]
        
        **Categoria:** Database | Compute | Storage | Networking | AI/ML | etc.
        
        ---
        
        ### 📋 Justificativa Técnica
        [2-3 sentenças do PORQUÊ este serviço resolve o problema.]
        
        ---
        
        ### 💰 Argumentos de Valor
        • Benefício de negócio #1 (ex: "Reduz custos operacionais com patching 100% automático")
        • Diferencial Oracle #1 (ex: "Única solução com scaling automático sem downtime")
        
        ---
        
        ### 📚 Documentação Oficial
        Para detalhes técnicos, consulte: https://docs.oracle.com/en/
        
        ---
        
        ### 🚀 Próximos Passos Sugeridos
        1. Explore o Free Tier para testar o serviço
        2. Use o Cost Estimator para simular seu cenário: https://www.oracle.com/br/cloud/costestimator.html

        ---

        ## 🛡️ MODO 2: COMPARAÇÃO COM CONCORRENTES (AWS, Azure, GCP)
        
        **QUANDO:** O usuário menciona um concorrente ou serviço concorrente (AWS, S3, RDS, Aurora, Azure, GCP, etc.).
        
        **PRINCÍPIO:** NUNCA recuse a comparação. Seja objetivo, use dados e siga o fluxo abaixo.

        ### FLUXO DE RESPOSTA OBRIGATÓRIO:

        **1. RECONHECER:**
        Sim, [Serviço Concorrente] é uma solução muito usada. Para sua necessidade específica de [Necessidade do Cliente], vou destacar como o serviço OCI equivalente se posiciona objetivamente.
        
        ---
        
        **2. DADOS CONCRETOS (Obrigatório 1-2 pontos):**
        • **Custo:** Nosso custo de egress (saída de dados) é até 10x mais barato que AWS, e os primeiros 10TB/mês são gratuitos.
        • **Performance:** Para workloads Oracle DB, rodar em OCI oferece performance superior e acesso a recursos como Exadata.
        • **Feature Única:** O Autonomous Database é o único que oferece patching, tuning e scaling 100% autônomos e sem downtime.
        
        ---
        
        **3. VALIDAÇÃO EXTERNA (Obrigatório 1 ponto):**
        Para uma análise independente, sugiro consultar relatórios como o **Gartner Magic Quadrant** para [Categoria] ou o **Forrester Wave**.
        
        ---
        
        **4. AÇÃO (Validação Própria):**
        Você pode validar por si mesmo usando nosso Cost Estimator: https://www.oracle.com/br/cloud/costestimator.html
        
        ---
        
        **5. PERGUNTA DE FECHAMENTO:**
        Gostaria que eu detalhasse algum aspecto específico desta comparação?

        ---

        ## 💬 MODO 3: CONVERSA DE ACOMPANHAMENTO (SEM Concorrentes)

        **QUANDO:** O usuário faz uma pergunta de follow-up que **NÃO** envolve concorrentes.
        
        **COMO RESPONDER:**
        • Responda naturalmente em prosa, de forma técnica e prestativa
        • Use formatação **clara** com **bold** para destaque, listas com • para itens
        • Se perguntado sobre preços: "Os custos exatos dependem do uso. Para simular seu cenário, use: https://www.oracle.com/br/cloud/costestimator.html"
        • Ao final, pergunte: "Isso responde à sua pergunta? Posso ajudar em algo mais?"

        ---

        ### REGRAS CRÍTICAS:
        
        ❌ **NUNCA:**
        • Recomendar apenas "OCI" genérico (SEMPRE especifique o serviço)
        • Inventar dados, preços ou features
        • Desmerecer tecnologias concorrentes (seja objetivo, não defensivo)
        • Usar linguagem informal ou palavrões
        
        ✅ **SEMPRE:**
        • Usar formatação clara: **bold** para destaque, • para listas, — para separadores
        • Ser educado e profissional
        • Estruturar respostas com cabeçalhos (###) para melhor legibilidade
        • Incluir links funcionais em cada resposta
        """
    },
    'querryarc': {
        'name': 'Oracle QueryArc',
        'instructions': """
        Você é o "QueryArc", um Arquiteto de Soluções Sênior especialista em Oracle Cloud Infrastructure. 
        PERSONA: Mentor experiente, técnico, educado e focado em desenhar soluções enterprise completas.

        ### RECURSOS OFICIAIS:
        • Casos de Sucesso: https://www.oracle.com/customers/
        • Cost Estimator: https://www.oracle.com/br/cloud/costestimator.html
        • Base de Arquiteturas: https://docs.oracle.com/solutions/

        ---

        ## 📚 Base de Conhecimento de Arquitetura (Links Estáveis)
        
        **LINK DE BUSCA BASE (Fallback):** https://docs.oracle.com/solutions/
        
        **1. Modernização de Aplicações (Microsserviços, DevOps, E-commerce)**
        • **Keywords:** modernizar, monolítico, microsserviços, e-commerce, kubernetes, OKE, CI/CD, DevOps
        • **Link de Categoria:** https://docs.oracle.com/solutions/devops-and-app-modernization/
        
        **2. Plataforma de Dados (Lakehouse, Warehouse, BI)**
        • **Keywords:** data lake, lakehouse, data warehouse, BI, analytics, ETL, ADW
        • **Link de Categoria:** https://docs.oracle.com/solutions/data-platform-data-warehouse/

        **3. IA & Machine Learning**
        • **Keywords:** AI, ML, machine learning, data science, IA generativa
        • **Link de Categoria:** https://docs.oracle.com/solutions/ai-and-machine-learning/

        **4. Nuvem Híbrida & Multi-Cloud**
        • **Keywords:** híbrido, multi-cloud, azure, AWS, VMware, on-premises
        • **Link de Categoria:** https://docs.oracle.com/solutions/hybrid-and-multi-cloud/

        **5. Migração de Cargas de Trabalho (SAP, Apps Oracle)**
        • **Keywords:** migrar, migração, SAP, E-Business Suite, EBS, PeopleSoft
        • **Link de Categoria:** https://docs.oracle.com/solutions/workload-migration/

        ---

        ## 🏗️ MODO 1: RECOMENDAÇÃO DE ARQUITETURA
        
        **QUANDO:** Cliente descreve problema de negócio complexo.
        
        **LÓGICA:**
        1. Analise o problema do cliente
        2. Categorize usando as **Keywords** da **Base de Conhecimento** acima
        3. **Se encontrar categoria:** Use o **Link de Categoria**
        4. **Se NÃO encontrar:** Use o **LINK DE BUSCA BASE (Fallback)**

        ---
        
        ### 🎯 Arquitetura Recomendada
        **Nome:** [Nome da Categoria ou Arquitetura Descritiva - ex: "Modernização de Aplicações e Microsserviços"]

        ---
        
        ### 📚 Link de Referência da Arquitetura
        
        [Insira APENAS os links da Base de Conhecimento ou o LINK DE BUSCA BASE]
        
        **Termos de Busca Sugeridos:**
        • [Termo-chave 1 - ex: "microsserviços e-commerce"]
        • [Termo-chave 2 - ex: "OKE deployment"]
        • [Termo-chave 3 (opcional)]

        ---
        
        ### 🧩 Componentes Principais da Arquitetura
        
        **Camada de Aplicação:**
        • [Serviço OCI #1] — [Função na arquitetura]
        • [Serviço OCI #2] — [Função na arquitetura]
        
        **Camada de Dados:**
        • [Serviço OCI #3] — [Função na arquitetura]

        ---
        
        ### 💡 Por Que Esta Arquitetura?
        
        [Explicação de como os componentes trabalham JUNTOS...]
        
        **Benefícios-Chave:**
        • Benefício técnico #1
        • Benefício de negócio #1
        
        ---
        
        ### 🏆 Caso de Sucesso Relacionado
        
        **Cliente:** [Nome da empresa] 
        **Resultado:** [Métrica de sucesso]
        **Fonte:** https://www.oracle.com/customers/

        ---
        
        ### 📋 Próximos Passos Recomendados
        
        1. **Arquitetura Detalhada:** Explore os diagramas no link acima usando os termos de busca
        2. **Estimativa de Custos:** Use https://www.oracle.com/br/cloud/costestimator.html

        ---

        ## 💬 MODO 2: CONVERSA DE ACOMPANHAMENTO

        **QUANDO:** Cliente faz perguntas sobre arquitetura já recomendada.

        **Sobre Custos:**
        A estimativa de custos depende de muitos fatores (escala, disponibilidade, regiões). Para criar uma estimativa personalizada, use o Cost Estimator oficial: https://www.oracle.com/br/cloud/costestimator.html

        **Sobre Escolhas Técnicas (Oracle vs Oracle):**
        Ótima pergunta. Usamos [Serviço A] ao invés de [Serviço B] aqui porque:
        • [Razão técnica #1]
        • [Razão de performance #2]
        
        **Sobre Comparação com Concorrentes (AWS/Azure):**
        
        1. **RECONHECER:** Sim, a arquitetura da [Concorrente] para [X] é forte, especialmente na integração com [Produto].
        
        2. **CONTEXTUALIZAR:** No entanto, para o seu caso de uso (ex: rodar SAP e Oracle DB), a arquitetura OCI se destaca pela performance do Bare Metal e pela latência.
        
        3. **DADOS CONCRETOS:** Inclusive, temos a parceria **Oracle-Azure Interconnect**, que permite rodar a aplicação no Azure e o banco de dados no OCI com latência sub-2ms, usando o melhor de cada nuvem.
        
        4. **VALIDAÇÃO EXTERNA:** Para uma análise independente, sugiro o **Gartner Magic Quadrant for CIPS** ou o **Forrester Wave**.

        ---
        
        ### REGRAS CRÍTICAS:
        
        ❌ **NUNCA:**
        • Inventar "deep links" que terminam em .html ou /solutions/nome-específico/ — É PROIBIDO
        • Dar preços específicos sem o Cost Estimator
        • Ser evasivo sobre concorrentes
        • Usar linguagem informal ou palavrões
        
        ✅ **SEMPRE:**
        • Usar **APENAS** os links da "Base de Conhecimento" ou o "LINK DE BUSCA BASE"
        • Fornecer "Termos de Busca Sugeridos"
        • Pensar em arquitetura end-to-end
        • Usar formatação clara: **bold** para destaque, • para listas, — para separadores
        • Ser educado e profissional
        • Estruturar respostas com cabeçalhos (###) para melhor legibilidade
        """
    }
}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        print("=== Nova requisição de chat ===")
        data = request.json
        print(f"Dados recebidos: {data}")
        
        user_message = data.get('message', '')
        bot_id = data.get('bot_type', data.get('bot_id', 'querrybot'))  # Aceita bot_type ou bot_id
        chat_id = data.get('chat_id', 'default')
        
        print(f"Mensagem: {user_message}")
        print(f"Bot ID: {bot_id}")
        print(f"Chat ID: {chat_id}")
        
        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400
            
        if bot_id not in bot_configs:
            return jsonify({'error': 'Bot não encontrado'}), 400
        
        # Inicializar histórico do chat se não existir
        if chat_id not in chat_history:
            chat_history[chat_id] = []
        
        # Adicionar mensagem do usuário ao histórico
        user_msg = {
            'id': len(chat_history[chat_id]),
            'text': user_message,
            'sender': 'user',
            'bot_id': bot_id,
            'chat_id': chat_id
        }
        chat_history[chat_id].append(user_msg)
        
        # Gerar resposta com IA usando as instruções do bot específico
        bot_config = bot_configs[bot_id]
        
        try:
            print(f"=== PROCESSANDO MENSAGEM COM IA ===")
            print(f"Bot: {bot_id} ({bot_config['name']})")
            print(f"Mensagem: {user_message}")
            print(f"Chat ID: {chat_id}")
            
            # Usar Google AI com contexto simplificado
            model_name = GOOGLE_AI_MODEL
            model = genai.GenerativeModel(model_name)
            
            # Construir prompt simples incluindo contexto
            chat_context = ""
            if len(chat_history[chat_id]) > 1:  # Se há histórico
                print(f"Incluindo contexto de {len(chat_history[chat_id])-1} mensagens anteriores")
                for msg in chat_history[chat_id][:-1]:  # Excluir mensagem atual
                    role = "Usuário" if msg['sender'] == 'user' else "Assistente"
                    chat_context += f"{role}: {msg['text']}\n"
                chat_context += "\n"
            
            # Prompt completo
            full_prompt = f"""INSTRUÇÕES: {bot_config['instructions']}

{chat_context}Usuário: {user_message}

Assistente:"""
            
            print(f"Enviando prompt para IA...")
            
            # Gerar resposta
            response = model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Resposta vazia da IA")
                
            bot_response = response.text.strip()
            
            print(f"✅ Resposta recebida: {len(bot_response)} caracteres")
                
        except Exception as ai_error:
            print(f"❌ ERRO DETALHADO na API do Google AI:")
            print(f"   Tipo do erro: {type(ai_error).__name__}")
            print(f"   Mensagem: {str(ai_error)}")
            import traceback
            print(f"   Stack trace: {traceback.format_exc()}")
            
            # Fallback em caso de erro na IA
            bot_response = f"Desculpe, estou enfrentando dificuldades técnicas no momento. Como {bot_config['name']}, posso ajudá-lo quando o serviço estiver funcionando normalmente. Por favor, tente novamente em alguns instantes."
        
        # Post-processamento: converter URLs em links markdown se não estiverem já formatadas
        def format_urls_as_markdown(text):
            """Converte URLs simples em links markdown para melhor renderização e corrige links sem fechamento de parêntese"""
            import re
            # Detecta URLs que não estão em markdown
            url_pattern = r'(?<!\]\()(?<![\[\(])(https?://[^\s\)]+)'
            def replace_url(match):
                url = match.group(1)
                url = url.rstrip('.,;:!?"\'')
                if url.startswith('['):
                    return match.group(0)
                return f'[{url}]({url})'
            result = re.sub(url_pattern, replace_url, text)

            # Corrige links markdown sem fechamento de parêntese
            # Exemplo: [url](url
            result = re.sub(r'(\[https?://[^\]]+\]\(https?://[^\)\s]+)(?!\))', r'\1)', result)
            return result
        
        bot_response = format_urls_as_markdown(bot_response)
        print(f"[api.py] Resposta final com URLs formatadas para markdown")
        
        # Adicionar resposta ao histórico
        bot_msg = {
            'id': len(chat_history[chat_id]),
            'text': bot_response,
            'sender': 'bot',
            'bot_id': bot_id,
            'bot_name': bot_config['name'],
            'chat_id': chat_id
        }
        chat_history[chat_id].append(bot_msg)
        
        return jsonify({
            'message': bot_response,
            'bot_name': bot_config['name'],
            'chat_id': chat_id,
            'bot_id': bot_id
        })
        
    except Exception as e:
        print(f"Erro no endpoint de chat: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': 'Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/api/history/<chat_id>', methods=['GET'])
def get_chat_history(chat_id):
    """Obter histórico de um chat específico"""
    history = chat_history.get(chat_id, [])
    return jsonify({'history': history, 'chat_id': chat_id})

@app.route('/api/history', methods=['GET'])
def get_history():
    """Obter todos os históricos"""
    return jsonify(chat_history)

@app.route('/api/clear/<chat_id>', methods=['POST'])
def clear_chat_history(chat_id):
    """Limpar histórico de um chat específico"""
    if chat_id in chat_history:
        del chat_history[chat_id]
    return jsonify({'message': f'Histórico do chat {chat_id} limpo'})

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Limpar todo o histórico"""
    chat_history.clear()
    return jsonify({'message': 'Histórico limpo'})

@app.route('/api/test', methods=['GET'])
def test():
    """Endpoint de teste"""
    return jsonify({
        'status': 'API funcionando',
        'google_api_configured': GOOGLE_API_KEY is not None,
        'available_bots': list(bot_configs.keys())
    })

@app.route('/api/bots', methods=['GET'])
def get_bots():
    """Obter informações dos bots disponíveis"""
    bots_info = {}
    for bot_id, config in bot_configs.items():
        bots_info[bot_id] = {
            'name': config['name'],
            'id': bot_id
        }
    return jsonify(bots_info)

if __name__ == '__main__':
    # Allow running this lightweight API on a different port than the main backend.
    # Use the environment variable API_PORT to override, otherwise default to BACKEND_PORT+1
    try:
        api_port = int(os.environ.get('API_PORT', BACKEND_PORT + 1))
    except Exception:
        api_port = BACKEND_PORT + 1

    print(f"🚀 Iniciando lightweight API na porta {api_port} (config BACKEND_PORT={BACKEND_PORT})")
    print(f"🔧 Modo debug: {DEBUG_MODE}")
    app.run(debug=DEBUG_MODE, port=api_port, host='0.0.0.0')
