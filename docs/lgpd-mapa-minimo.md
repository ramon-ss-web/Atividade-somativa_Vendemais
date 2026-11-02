# Mapa LGPD mínimo — demo acadêmico (não substitui jurídico da VendeMais)

| Campo | Conteúdo |
| ----- | -------- |
| Tratamento | Enrichment de **empresa** (nome fantasia / razão) para score ICP |
| Titular no demo | Ninguém — usar só `Acme Logística SA` e IDs falsos |
| Categorias | Nome de empresa, snippets públicos de busca, JSON inferido pelo LLM |
| **Não** tratar | CPF, e-mail de pessoa, telefone, proposta comercial confidencial |
| Operadores no fluxo herdado | Google (CSE), fornecedor LLM (OpenAI EUA), Airtable, HubSpot, GitHub, HF Spaces |
| Transferência internacional | Sim, no desenho original (Joana). No demo Etapa 1 o smoke **mock** evita enviar dado a OpenAI |
| Base legal (negócio, para o pitch) | Execução de contrato B2B / legítimo interesse de inteligência comercial — **validar com jurídico**; aluno não inventa parecer |
| Minimização Etapa 1 | Sem `raw_search_results` no Space; truncar snippet (teste Python) |
| DPA | Backlog (OpenAI + Google) — item 8 de `docs/o-que-precisa-construir.md` |

Uma frase para o vídeo: “O dado de cliente real não entra na URL pública.”
