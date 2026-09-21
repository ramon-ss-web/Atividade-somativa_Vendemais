1. Detectar deal em `appointmentscheduled` *(no demo: webhook com payload sintético — poll HubSpot permanece dívida documentada)*
2. Google Custom Search (5 resultados)
3. LLM devolve JSON: industry, tech_stack, buying_signals, **icp_match_score** 0–100, talking_points
4. Gravar Airtable `Lead Enrichment`
5. Atualizar o deal no HubSpot
## Como importar / rodar — mirror n8n (teste local)
**O que mudou na Etapa 1 (evolução):** documentação de decisão (auditoria, matriz, ADRs, C4), GitHub Actions validando os JSON, Dockerfile de publicação, secrets fora do runtime público (smoke usa o workflow **offline**).
**O que não mudou de propósito:** os 5 passos, o schema Airtable, o blueprint Make versionado em `workflows/`.
---
## Como rodar
### A) Produção do curso (URL pública)
Quando `docs/publicacao.md` tiver a URL do Space:
```bash
curl -X POST "https://COLE-A-URL-DO-SPACE/webhook/lead-enrich-local" \
  -H "Content-Type: application/json" \
  -d "{\"deal_id\": \"9876543210\", \"company\": \"Acme Logística SA\"}"
```
Esperado: HTTP 200 e `icp_match_score` **60** (mock determinístico para este `deal_id`). Cold start do free tier: ~1 min no primeiro hit.
### B) Local (handoff da Joana + smoke da Etapa 1)
```bash
cd n8n-mirror
docker compose up -d          # sobe o n8n em http://localhost:5678
docker compose up -d          # n8n em http://localhost:5678
```
Depois: importe `n8n-mirror/workflows/vendemais-enrich-v0.json` pelo menu **Import from File**,
configure credenciais nos nodes, ative o workflow e dispare:
Importe `n8n-mirror/workflows/vendemais-enrich-local.json`, **Publish**, depois:
```bash
curl -X POST http://localhost:5678/webhook/lead-enrich \
curl -X POST http://localhost:5678/webhook/lead-enrich-local \
  -H "Content-Type: application/json" \
  -d '{"deal_id": "9876543210", "company": "Acme Logística SA"}'
  -d "{\"deal_id\": \"9876543210\", \"company\": \"Acme Logística SA\"}"
```
Passo a passo completo em [`n8n-mirror/README.md`](n8n-mirror/README.md).
O workflow `vendemais-enrich-v0.json` é o mirror **com** Google/OpenAI/Airtable/HubSpot (precisa de credenciais). Passo a passo: [`n8n-mirror/README.md`](./n8n-mirror/README.md).
## Como rodar os testes (não chamam API nenhuma)
### C) Testes (sem API, sem Docker)
```bash
python tests/validate_workflows.py      # estrutura dos 2 JSON
python tests/test_enrichment_logic.py   # prompt + parsing do fit-score (LLM mockado)
python tests/validate_workflows.py
python tests/test_enrichment_logic.py
```
## Sobre o LLM
### D) Make.com (contrato herdado — não é o host desta etapa)
Hoje é **um modelo GPT pequeno da OpenAI** (`temperature 0.3`, `max_tokens 1500`, `response_format: json_object`).
Dá pra trocar por **Anthropic Claude** sem mudar a arquitetura: no Make use o módulo
`anthropic:createMessage`; no n8n troque o node OpenAI por um **HTTP Request** batendo em
`https://api.anthropic.com/v1/messages` (mesmo system/user prompt). O JSON de saída é o mesmo.
1. Na **conta corporativa** VendeMais: Create scenario → Import Blueprint → `workflows/vendemais-make-blueprint.json`.
2. Reconfigure Connections na mão (`__IMTCONN__: 0` de propósito). Scheduler permanece **OFF** até a conta corporativa.
3. Teste pontual: **Run once**.
## Dívida técnica herdada
Variáveis de CI/n8n: copie `.env.example` → `.env` (nunca commitar).
Coisas que ficaram **propositalmente sem resolver** (é o que vocês vão corrigir no curso).
Estão aqui, marcadas, pra ninguém ser pego de surpresa. **Não "arrumei" nada disso** —
detalhes e ordem de urgência em [`docs/notas-joana.md`](docs/notas-joana.md).
---
1. **Scheduler OFF / roda manual.** No Make o trigger era poll de 15min, hoje desligado;
   alguém clica "Run once" todo dia. No mirror n8n o workflow vem `active: false` e você
   dispara via curl. Mesma realidade: nada roda sozinho.
2. **API key pessoal da Joana.** OpenAI no meu cartão (~US$ 18/mês), Google CSE no meu
   billing, Airtable PAT meu. No mirror tem até uma chave de exemplo *hardcoded* no JSON
   (não é real, mas mostra o anti-padrão). Tudo precisa virar conta corporativa.
3. **Zero tratamento de erro.** Se a OpenAI devolve JSON quebrado, o cenário morre
   silencioso (já aconteceu ~3x). Sem branch de falha, sem retry custom, sem alerta no Slack.
4. **Sem versionamento Git originalmente.** Foi tudo clicado no Make. Não havia export do
   blueprint nem histórico — esse repo é o primeiro passo pra mudar isso.
5. **Sem instrumentação de custo.** Não tem campo `cost_usd` no Airtable nem cálculo de
   tokens por execução. Prompts estouram 8k tokens (snippets do Google não são truncados).
   Impossível auditar custo por lead hoje.
6. **Sem mapa LGPD de transferência internacional.** Dados de empresa-cliente passam por
   Google + OpenAI nos EUA. Levantei a bandeira pro jurídico, nunca responderam.
7. **Schema Airtable problemático.** `tech_stack` como *Multiple select* explode opções
   (400+, duplicadas), sem unique constraint em `deal_id` (gera linhas duplicadas),
   `raw_search_results` pesado (~80% da quota). Ver [`docs/airtable-schema.md`](docs/airtable-schema.md).
## Arquitetura
## Avisos importantes (por favor lê isso)
Diagrama C4: [Nível 1 e 2](./docs/c4-niveis-1-2.md) (exporte PNG para `docs/c4/` no Excalidraw).
- O cenário Make tá no **meu espaço pessoal** (`joana@vendemais.com`). Vão precisar
  **migrar pra conta corporativa** — o Make não migra workspace, vocês recriam/importam blueprint.
```
GitHub (fonte) → Actions (CI) → Hugging Face Space (n8n)
                                      ├─ webhook mock (smoke $0)
                                      └─ webhook real (opcional, secrets)
Make blueprint JSON ───────────────► versionado, não hospeda a demo
HubSpot / Google / LLM / Airtable ─► externos (v0); mock no local
```
Árvore do repositório:
```
├── workflows/vendemais-make-blueprint.json
├── n8n-mirror/          docker-compose, Dockerfile, workflows v0 + local
├── tests/               validador JSON + lógica com LLM mockado
├── .github/workflows/ci.yml
├── docs/                auditoria, ADRs, C4, evidências, LGPD
├── BRIEFING.md · CHANGELOG.md · .env.example
```
O Make.com **não roda local**; o `n8n-mirror/` existe por isso.
---
## URL pública
| Ambiente | Onde preencher | Estado em 2026-09-21 |
| -------- | -------------- | -------------------- |
| Hugging Face Spaces | [`docs/publicacao.md`](./docs/publicacao.md) | PENDENTE |
| GitHub Actions | idem | PENDENTE (YAML já no repo) |
| Vídeo 3–5 min | idem + [`docs/roteiro-demonstracao.md`](./docs/roteiro-demonstracao.md) | PENDENTE |
---
## Dívida técnica aceita (não esconda)
Etapa 1 **não** fecha: scheduler HubSpot, DPA jurídico, Looker, unique `deal_id`, Slack, `cost_usd`. Lista original da Joana abaixo; urgência em [`docs/notas-joana.md`](./docs/notas-joana.md). Checklist do desafio de 12 semanas: [`docs/o-que-precisa-construir.md`](./docs/o-que-precisa-construir.md). Mapa LGPD do demo: [`docs/lgpd-mapa-minimo.md`](./docs/lgpd-mapa-minimo.md).
### LLM (herdado)
Modelo GPT pequeno da OpenAI (`temperature 0.3`, `max_tokens 1500`, `response_format: json_object`). Dá para trocar por Anthropic sem mudar a arquitetura: Make `anthropic:createMessage`; n8n HTTP Request em `https://api.anthropic.com/v1/messages`. O JSON de saída é o mesmo. No smoke da Etapa 1 **nenhuma** chamada é feita (Code nodes mockados).
---
<details>
<summary>Passagem de bastão da Joana (texto original do handoff)</summary>
Oi! Sou a Joana 👋
Esse era meu projeto de estágio na VendeMais (durou um semestre). Foi pra produção no fim daquele semestre e tá rodando — bom, *tava* rodando, agora eu acho que a Cláudia desligou porque saiu do meu controle quando eu fui embora.
### O que é
Um cenário no **Make.com** (Stack C) que:
1. Observa novos deals no HubSpot que entram em `appointmentscheduled`
2. Pesquisa a empresa no Google Search
3. Manda resultados pro OpenAI (um modelo GPT pequeno) gerar um JSON com industry, tech stack, ICP score etc.
4. Grava o resultado numa tabela do Airtable
5. Atualiza o deal no HubSpot com o `icp_match_score`
São **5 módulos** em linha: HubSpot → Google → OpenAI → Airtable → HubSpot.
### Dívida técnica herdada
Coisas que ficaram **propositalmente sem resolver** (é o que vocês vão corrigir no curso). Estão aqui, marcadas, pra ninguém ser pego de surpresa. **Não "arrumei" nada disso** — detalhes e ordem de urgência em [`docs/notas-joana.md`](./docs/notas-joana.md).
1. **Scheduler OFF / roda manual.** No Make o trigger era poll de 15min, hoje desligado; alguém clica "Run once" todo dia. No mirror n8n o workflow vem `active: false` e você dispara via curl. Mesma realidade: nada roda sozinho.
2. **API key pessoal da Joana.** OpenAI no cartão (~US$ 18/mês), Google CSE no billing dela, Airtable PAT dela. No mirror tem até uma chave de exemplo *hardcoded* no JSON (não é real, mas mostra o anti-padrão). Tudo precisa virar conta corporativa.
3. **Zero tratamento de erro.** Se a OpenAI devolve JSON quebrado, o cenário morre silencioso (já aconteceu ~3x). Sem branch de falha, sem retry custom, sem alerta no Slack.
4. **Sem versionamento Git originalmente.** Foi tudo clicado no Make. Não havia export do blueprint nem histórico — esse repo é o primeiro passo pra mudar isso.
5. **Sem instrumentação de custo.** Não tem campo `cost_usd` no Airtable nem cálculo de tokens por execução. Prompts estouram 8k tokens (snippets do Google não são truncados). Impossível auditar custo por lead hoje.
6. **Sem mapa LGPD de transferência internacional.** Dados de empresa-cliente passam por Google + OpenAI nos EUA. Levantei a bandeira pro jurídico, nunca responderam.
7. **Schema Airtable problemático.** `tech_stack` como *Multiple select* explode opções (400+, duplicadas), sem unique constraint em `deal_id` (gera linhas duplicadas), `raw_search_results` pesado (~80% da quota). Ver [`docs/airtable-schema.md`](./docs/airtable-schema.md).
### Avisos importantes
- O cenário Make tá no **espaço pessoal** (`joana@vendemais.com`). Vão precisar **migrar pra conta corporativa** — o Make não migra workspace; recriam/importam blueprint.
- As **conexões não saem** no blueprint JSON do Make (tem que reconfigurar OAuth/PAT na mão).
- Anexei **screenshots descritos em texto** em `docs/cenario-make-screenshots/` e o
  **pseudo-blueprint** em `make-blueprint-pseudo.txt` (foi a base do JSON real).
- Screenshots descritos em texto em `docs/cenario-make-screenshots/` e **pseudo-blueprint** em `make-blueprint-pseudo.txt`.
## Se travarem
### Se travarem
Me chama no LinkedIn (Joana M.), respondo quando puder. Tô em Lisboa fazendo mestrado, fuso +4h.
Boa sorte! O projeto é bem legal, os AEs amam o score. 💛
— Joana
</details>