import urllib.request
import json

url = 'http://localhost:5678/webhook-test/lead-enrich-local'
data = {
    "deal_id": "9876543210",
    "company": "Acme Logística SA"
}

req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), {'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(f"✅ Disparo feito com sucesso! Status: {response.status}")
except Exception as e:
    print(f"❌ Erro ao disparar: {e}")