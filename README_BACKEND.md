# Backend - Cloud Solution Advisor

Este diretório contém o backend da aplicação Cloud Solution Advisor.

## 📁 Estrutura

```
backend/
├── api.py              # API principal Flask com endpoints dos bots
├── api_simple.py       # API simplificada para testes
└── requirements.txt    # Dependências Python
```

## 🚀 Como Executar

### Opção 1: Script Automático
```bash
# Na raiz do projeto
.\start-backend.bat
```

### Opção 2: Manual
```bash
cd backend
pip install -r requirements.txt
python api.py
```

## 🔧 Configuração

O backend utiliza as configurações centralizadas em `../config.py`:

- **Porta**: 5000 (padrão)
- **Google AI Model**: gemini-2.0-flash-exp
- **CORS**: Habilitado para desenvolvimento

## 📡 Endpoints da API

- `GET /api/test` - Verifica se a API está funcionando
- `POST /api/chat` - Enviar mensagem para os bots
- `GET /api/history/<chat_id>` - Obter histórico de um chat
- `GET /api/bots` - Listar bots disponíveis

## 🤖 Bots Disponíveis

1. **QueryBot** (`querrybot`)
   - Especialista em soluções Oracle Cloud
   - Recomenda serviços específicos

2. **QueryArc** (`querryarc`)
   - Arquiteto de soluções sênior
   - Recomenda arquiteturas de referência

## 🛠️ Desenvolvimento

Para desenvolvimento, a API roda em modo debug habilitado com hot-reload automático.

## 📋 Dependências Principais

- Flask - Framework web
- Flask-CORS - Suporte a CORS
- google-generativeai - Integração com Google AI