#!/usr/bin/env python3
"""
Teste de fluxo de conversa para verificar se o contexto está funcionando corretamente.
Testa cenários de conversa com múltiplas mensagens para QuerryBot e QuerryArc.
"""

import requests
import json
import time

# Configuração da API
API_URL = "http://127.0.0.1:5000"

def enviar_mensagem(bot_type, message, chat_id="test_session"):
    """Envia uma mensagem para o bot e retorna a resposta"""
    try:
        payload = {
            "message": message,
            "bot_type": bot_type,
            "chat_id": chat_id
        }
        
        response = requests.post(f"{API_URL}/api/chat", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status: {response.status_code}, Response: {response.text}"}
            
    except Exception as e:
        return {"error": str(e)}

def teste_conversa_querrybot():
    """Testa uma conversa com contexto no QuerryBot"""
    print("🤖 TESTE QUERRYBOT - Conversa com Contexto")
    print("=" * 50)
    
    chat_id = "test_querrybot_context"
    
    # Primeira mensagem - problema novo (Mode 1)
    print("\n1. Primeira pergunta (Mode 1 esperado):")
    response1 = enviar_mensagem("querrybot", "Preciso migrar minha aplicação para Oracle Cloud", chat_id)
    print(f"Resposta: {response1.get('response', response1)}")
    
    time.sleep(1)
    
    # Segunda mensagem - follow-up (Mode 2)
    print("\n2. Pergunta de follow-up (Mode 2 esperado):")
    response2 = enviar_mensagem("querrybot", "Quanto custa?", chat_id)
    print(f"Resposta: {response2.get('response', response2)}")
    
    time.sleep(1)
    
    # Terceira mensagem - mais detalhes (Mode 2)
    print("\n3. Mais detalhes (Mode 2 esperado):")
    response3 = enviar_mensagem("querrybot", "E qual é o processo de migração?", chat_id)
    print(f"Resposta: {response3.get('response', response3)}")
    
    return response1, response2, response3

def teste_conversa_querryarc():
    """Testa uma conversa com contexto no QuerryArc"""
    print("\n🏗️ TESTE QUERRYARC - Conversa com Contexto")
    print("=" * 50)
    
    chat_id = "test_querryarc_context"
    
    # Primeira mensagem - problema novo (Mode 1)
    print("\n1. Primeira pergunta (Mode 1 esperado):")
    response1 = enviar_mensagem("querryarc", "Como fazer arquitetura de microserviços na Oracle Cloud?", chat_id)
    print(f"Resposta: {response1.get('response', response1)}")
    
    time.sleep(1)
    
    # Segunda mensagem - follow-up (Mode 2)
    print("\n2. Pergunta de follow-up (Mode 2 esperado):")
    response2 = enviar_mensagem("querryarc", "Quais serviços usar para banco de dados?", chat_id)
    print(f"Resposta: {response2.get('response', response2)}")
    
    time.sleep(1)
    
    # Terceira mensagem - mais detalhes (Mode 2)
    print("\n3. Mais detalhes (Mode 2 esperado):")
    response3 = enviar_mensagem("querryarc", "Como configurar a rede entre os serviços?", chat_id)
    print(f"Resposta: {response3.get('response', response3)}")
    
    return response1, response2, response3

def verificar_contexto():
    """Verifica se o histórico está sendo mantido"""
    print("\n📜 VERIFICAÇÃO DE HISTÓRICO")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_URL}/api/history/test_querrybot_context")
        if response.status_code == 200:
            history = response.json()
            print(f"Histórico QuerryBot: {len(history.get('history', []))} mensagens")
            for i, msg in enumerate(history.get('history', [])[:6]):  # Primeiras 6
                print(f"  {i+1}. {msg.get('role', 'unknown')}: {msg.get('parts', [''])[0][:100]}...")
        else:
            print(f"Erro ao buscar histórico: {response.status_code}")
            
        response = requests.get(f"{API_URL}/api/history/test_querryarc_context")
        if response.status_code == 200:
            history = response.json()
            print(f"Histórico QuerryArc: {len(history.get('history', []))} mensagens")
            for i, msg in enumerate(history.get('history', [])[:6]):  # Primeiras 6
                print(f"  {i+1}. {msg.get('role', 'unknown')}: {msg.get('parts', [''])[0][:100]}...")
                
    except Exception as e:
        print(f"Erro ao verificar histórico: {e}")

def main():
    print("🚀 TESTE DE FLUXO DE CONVERSA COM CONTEXTO")
    print("=" * 60)
    print("Verificando se os bots mantêm contexto e distinguem Mode 1 vs Mode 2")
    
    # Testa API básica
    try:
        response = requests.get(f"{API_URL}/api/test")
        if response.status_code != 200:
            print(f"❌ API não está respondendo: {response.status_code}")
            return
        print("✅ API está respondendo")
    except Exception as e:
        print(f"❌ Erro ao conectar com API: {e}")
        return
    
    # Executa testes
    querrybot_responses = teste_conversa_querrybot()
    querryarc_responses = teste_conversa_querryarc()
    
    # Verifica histórico
    verificar_contexto()
    
    print("\n🎯 ANÁLISE DOS RESULTADOS")
    print("=" * 50)
    print("Verifique se:")
    print("1. Primeira mensagem tem formato Mode 1 (PROBLEMA + ANÁLISE + SOLUÇÕES)")
    print("2. Mensagens seguintes são Mode 2 (resposta direta baseada no contexto)")
    print("3. Respostas mantêm contexto da conversa anterior")
    print("4. Bots não usam termos proibidos (OCI para QuerryBot)")
    print("5. Histórico foi criado e mantido para ambas as conversas")

if __name__ == "__main__":
    main()