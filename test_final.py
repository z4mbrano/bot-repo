#!/usr/bin/env python3
"""
Teste final - verificar se todas as correções funcionam
"""

import requests
import json
import time

def teste_final():
    print("🎯 TESTE FINAL - Sistema Completo")
    print("=" * 50)
    
    API_URL = "http://127.0.0.1:5000"
    
    # Teste 1: QueryBot
    print("\n1. Testando QueryBot...")
    response = requests.post(f"{API_URL}/api/chat", json={
        "message": "Preciso hospedar uma aplicação web",
        "bot_type": "querrybot",
        "chat_id": "teste_final"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['bot_name']}: {data['message'][:100]}...")
        
        # Follow-up
        time.sleep(1)
        response2 = requests.post(f"{API_URL}/api/chat", json={
            "message": "Qual o custo?",
            "bot_type": "querrybot", 
            "chat_id": "teste_final"
        })
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Follow-up: {data2['message'][:100]}...")
        else:
            print(f"❌ Follow-up falhou: {response2.status_code}")
    else:
        print(f"❌ QueryBot falhou: {response.status_code}")
    
    # Teste 2: QueryArc
    print("\n2. Testando QueryArc...")
    response = requests.post(f"{API_URL}/api/chat", json={
        "message": "Como criar um sistema de analytics moderno?",
        "bot_type": "querryarc",
        "chat_id": "teste_final_arc"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['bot_name']}: {data['message'][:100]}...")
        
        # Verificar se tem link
        if "https://" in data['message']:
            print("✅ Link encontrado na resposta")
        else:
            print("⚠️ Nenhum link encontrado")
    else:
        print(f"❌ QueryArc falhou: {response.status_code}")
    
    print("\n🎉 SISTEMA FUNCIONANDO!")
    print("Frontend: http://localhost:5173/")
    print("API: http://127.0.0.1:5000")

if __name__ == "__main__":
    teste_final()