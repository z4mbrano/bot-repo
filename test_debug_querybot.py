#!/usr/bin/env python3
"""
Teste específico para depurar o problema do QueryBot com histórico de conversa.
"""

import requests
import json
import time

API_URL = "http://127.0.0.1:5000"

def teste_querrybot_debug():
    """Teste detalhado do QueryBot para identificar o problema de histórico"""
    print("🔍 TESTE DEBUG - QueryBot com Histórico")
    print("=" * 60)
    
    chat_id = "debug_querrybot"
    
    # Teste 1: Primeira mensagem (deve funcionar)
    print("\n1️⃣ TESTE: Nova necessidade (Mode 1)")
    print("-" * 40)
    
    payload1 = {
        "message": "Preciso de um banco de dados para minha aplicação",
        "bot_type": "querrybot",
        "chat_id": chat_id
    }
    
    print(f"Enviando: {payload1}")
    
    try:
        response1 = requests.post(f"{API_URL}/api/chat", json=payload1, timeout=30)
        print(f"Status Code: {response1.status_code}")
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"✅ Sucesso: {data1.get('bot_name', 'Unknown')}")
            print(f"Resposta: {data1.get('message', 'Sem resposta')[:200]}...")
        else:
            print(f"❌ Erro: {response1.text}")
            return
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return
    
    time.sleep(2)
    
    # Teste 2: Follow-up (aqui que falha)
    print("\n2️⃣ TESTE: Pergunta de follow-up (Mode 2)")
    print("-" * 40)
    
    payload2 = {
        "message": "Por que você escolheu essa opção?",
        "bot_type": "querrybot", 
        "chat_id": chat_id
    }
    
    print(f"Enviando: {payload2}")
    
    try:
        response2 = requests.post(f"{API_URL}/api/chat", json=payload2, timeout=30)
        print(f"Status Code: {response2.status_code}")
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Sucesso: {data2.get('bot_name', 'Unknown')}")
            print(f"Resposta: {data2.get('message', 'Sem resposta')[:200]}...")
        else:
            print(f"❌ Erro: {response2.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Verificar histórico
    print("\n3️⃣ VERIFICAÇÃO: Histórico")
    print("-" * 40)
    
    try:
        history_response = requests.get(f"{API_URL}/api/history/{chat_id}")
        if history_response.status_code == 200:
            history_data = history_response.json()
            history = history_data.get('history', [])
            print(f"Histórico contém {len(history)} mensagens:")
            
            for i, msg in enumerate(history):
                sender = msg.get('sender', 'unknown')
                text = msg.get('text', '')[:100]
                print(f"  {i+1}. {sender}: {text}...")
        else:
            print(f"❌ Erro ao buscar histórico: {history_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar histórico: {e}")

def teste_querryarc_comparacao():
    """Teste do QueryArc para comparar comportamento"""
    print("\n🏗️ TESTE COMPARAÇÃO - QueryArc")
    print("=" * 60)
    
    chat_id = "debug_querryarc"
    
    # Teste básico do QueryArc
    payload = {
        "message": "Como criar um data lake moderno?",
        "bot_type": "querryarc",
        "chat_id": chat_id
    }
    
    try:
        response = requests.post(f"{API_URL}/api/chat", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ QueryArc funcionou: {data.get('bot_name', 'Unknown')}")
            print(f"Resposta: {data.get('message', 'Sem resposta')[:200]}...")
        else:
            print(f"❌ QueryArc também falhou: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro no QueryArc: {e}")

def main():
    print("🚨 DEBUG DO PROBLEMA DO QUERYBOT")
    print("=" * 60)
    print("Verificando se a API está online...")
    
    try:
        test_response = requests.get(f"{API_URL}/api/test", timeout=10)
        if test_response.status_code != 200:
            print(f"❌ API não está funcionando: {test_response.status_code}")
            return
        print("✅ API está online")
    except Exception as e:
        print(f"❌ Não foi possível conectar à API: {e}")
        return
    
    # Executar testes
    teste_querrybot_debug()
    teste_querryarc_comparacao()
    
    print("\n🎯 ANÁLISE")
    print("=" * 60)
    print("Se o QueryBot falhar no follow-up mas funcionar na primeira mensagem,")
    print("o problema está na construção do histórico de conversa no backend.")
    print("Verifique os logs do servidor Python para mais detalhes.")

if __name__ == "__main__":
    main()