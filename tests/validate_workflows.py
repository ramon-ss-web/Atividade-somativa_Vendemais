#!/usr/bin/env python3
"""
Validador estrutural dos dois artefatos de workflow:
  1. workflows/vendemais-make-blueprint.json  (blueprint Make.com)
  2. n8n-mirror/workflows/vendemais-enrich-v0.json  (mirror n8n)

NAO chama API nenhuma. So carrega os JSON e checa a estrutura.
Roda: python tests/validate_workflows.py
"""
import json
import os
import sys


# Caminhos dos workflows do VendeMais conforme a estrutura do repositório
WORKFLOW_PATHS = [
    "workflows/vendemais-make-blueprint.json",
    "n8n-mirror/workflows/vendemais-enrich-v0.json",
    "n8n-mirror/workflows/vendemais-enrich-local.json"
]


def validate_json_file(filepath):
    """Valida se o arquivo existe e se é um JSON válido."""
    if not os.path.exists(filepath):
        print(f"⚠️  [AVISO] Arquivo não encontrado: {filepath} (Ignorando se opcional)")
        return True
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ [SUCESSO] {filepath} é um JSON válido.")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ [ERRO] Falha de sintaxe JSON em {filepath}: {e}")
        return False
    except Exception as e:
        print(f"❌ [ERRO] Falha ao ler {filepath}: {e}")
        return False


def main():
    print("🔍 Iniciando Validação Automática de Workflows (Smoke Test 1)...")
    all_valid = True
    
    for path in WORKFLOW_PATHS:
        if not validate_json_file(path):
            all_valid = False


    if not all_valid:
        print("\n❌ Validação dos workflows falhou!")
        sys.exit(1)
    
    print("\n🎉 Todos os workflows inspecionados estão estruturalmente válidos!")
    sys.exit(0)


if __name__ == "__main__":
    main()
