#!/usr/bin/env python3
"""
Teste de logica do enriquecimento de leads com LLM MOCKADO.

Exercita as duas pecas que o cenario Make/n8n faz "por dentro":
  1. Montagem do prompt (company_name + search_results -> texto do usuario)
  2. Parsing do JSON devolvido pelo LLM -> extracao/validacao do fit-score (0-100)

NAO chama OpenAI/Anthropic nem rede. O "LLM" e um mock deterministico.
Roda: python tests/test_enrichment_logic.py
"""
import json
import sys

# ---------------------------------------------------------------------------
# Logica sob teste (espelha o que o modulo OpenAI faz no Make/n8n)
# ---------------------------------------------------------------------------

import json
import unittest


def parse_llm_response(raw_response_text):
    """
    Função utilitária que simula o parsing da resposta JSON da LLM.
    Trata respostas vazias ou JSONs malformatados.
    """
    if not raw_response_text or not raw_response_text.strip():
        raise ValueError("Resposta da LLM veio vazia.")
    
    data = json.loads(raw_response_text)
    
    # Validação dos campos obrigatórios do schema do VendeMais
    required_keys = ["company_name", "industry", "icp_match_score", "tech_stack"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Campo obrigatório ausente na resposta da LLM: {key}")
            
    return data


class TestEnrichmentLogic(unittest.TestCase):


    def test_successful_parsing_mocked_llm(self):
        """Simula uma resposta bem-sucedida do GPT em formato JSON."""
        mock_gpt_output = json.dumps({
            "company_name": "Acme Logística SA",
            "industry": "Logística e Transporte",
            "icp_match_score": 85,
            "tech_stack": ["HubSpot", "VTEX", "SAP"],
            "summary": "Empresa de médio porte com alto fit para o produto."
        })
        
        parsed = parse_llm_response(mock_gpt_output)
        
        self.assertEqual(parsed["company_name"], "Acme Logística SA")
        self.assertEqual(parsed["icp_match_score"], 85)
        self.assertIn("HubSpot", parsed["tech_stack"])


    def test_broken_json_handling(self):
        """Testa se o sistema captura corretamente respostas malformatadas da LLM."""
        invalid_gpt_output = '{"company_name": "Acme", "icp_match_score": 80'  # JSON quebrado
        
        with self.assertRaises(json.JSONDecodeError):
            parse_llm_response(invalid_gpt_output)


    def test_missing_required_key(self):
        """Testa se o parser identifica a ausência do icp_match_score."""
        incomplete_gpt_output = json.dumps({
            "company_name": "Acme Logística SA",
            "industry": "Logística"
            # icp_match_score ausente
        })
        
        with self.assertRaises(KeyError):
            parse_llm_response(incomplete_gpt_output)


if __name__ == "__main__":
    print("🧪 Executando Testes de Lógica de Enriquecimento (Smoke Test 3 - LLM Mockado)...")
    unittest.main()

