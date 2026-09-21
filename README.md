# Lead Enrichment VendeMais

Pipeline de enriquecimento de leads para o VendeMais. O fluxo recebe um deal,
pesquisa a empresa, usa um LLM para estruturar os dados e grava o resultado no
Airtable e no HubSpot.

## Fluxo

1. Detectar um deal em `appointmentscheduled`.
2. Consultar o Google Custom Search (5 resultados).
3. Gerar JSON com `industry`, `tech_stack`, `buying_signals`,
   `icp_match_score` (0-100) e `talking_points`.
4. Gravar em `Lead Enrichment` no Airtable.
5. Atualizar o deal no HubSpot.

No demo, a etapa 1 usa um webhook com payload sintético. O polling do HubSpot
continua documentado como dívida técnica.

## Arquitetura

```text
GitHub (fonte) -> Actions (CI) -> Hugging Face Space (n8n)
                                      |- webhook mock (smoke sem custo)
                                      `- webhook real (opcional, com secrets)

Make blueprint JSON ----------------> versionado, não hospeda a demo
HubSpot / Google / LLM / Airtable -> externos no fluxo real; mock no local
```

O Make.com não roda localmente. O diretório `n8n-mirror/` fornece uma versão
local do fluxo e uma versão offline, sem credenciais nem chamadas pagas.

## Como rodar

### Demo pública

Quando a URL do Space estiver disponível, envie um payload para o webhook
offline:

```bash
curl -X POST "https://COLE-A-URL-DO-SPACE/webhook/lead-enrich-local" \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"9876543210","company":"Acme Logística SA"}'
```

O retorno esperado é HTTP 200 com `icp_match_score` igual a **60** para esse
`deal_id`. O primeiro acesso no free tier pode levar cerca de um minuto.

### Execução local offline

```bash
cd n8n-mirror
docker compose up -d
```

Abra `http://localhost:5678`, importe
`workflows/vendemais-enrich-local.json`, clique em **Publish** e execute:

```bash
curl -X POST http://localhost:5678/webhook/lead-enrich-local \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"9876543210","company":"Acme Logística SA"}'
```

### Mirror n8n com serviços reais

Importe `n8n-mirror/workflows/vendemais-enrich-v0.json`, configure as
credenciais nos nodes, ative o workflow e dispare:

```bash
curl -X POST http://localhost:5678/webhook/lead-enrich \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"9876543210","company":"Acme Logística SA"}'
```

O mirror real exige credenciais do Google, OpenAI, Airtable e HubSpot. Consulte
o passo a passo em [`n8n-mirror/README.md`](n8n-mirror/README.md).

## Testes

Os testes não chamam APIs externas:

```bash
python tests/validate_workflows.py
python tests/test_enrichment_logic.py
```

O workflow de CI em [`tests/github/workflows/ci.yml`](tests/github/workflows/ci.yml)
valida os JSON dos workflows e executa os testes mockados. Para variáveis locais,
copie `.env.example` para `.env` e nunca commite credenciais.

## Make.com e LLM

O contrato herdado usa um modelo GPT pequeno da OpenAI com `temperature 0.3`,
`max_tokens 1500` e `response_format: json_object`. O fluxo pode ser migrado
para Anthropic sem mudar o schema: use `anthropic:createMessage` no Make ou um
node HTTP Request para `https://api.anthropic.com/v1/messages` no n8n.

Para importar o cenário Make na conta corporativa:

1. Importe `workflows/vendemais-make-blueprint.json`.
2. Reconfigure manualmente as conexões (`__IMTCONN__: 0` é intencional).
3. Mantenha o scheduler desligado e use **Run once** para o teste pontual.

## Estrutura

```text
workflows/vendemais-make-blueprint.json
n8n-mirror/                  docker-compose, Dockerfile e workflows n8n
tests/                       validador JSON e lógica com LLM mockado
tests/github/workflows/ci.yml CI
docs/                        schema Airtable, notas e checklist do projeto
BRIEFING.md · CHANGELOG.md · .env.example
```

Documentação de schema e contexto: [`docs/airtable-schema.md`](docs/airtable-schema.md)
e [`docs/notas-joana.md`](docs/notas-joana.md).

## URL pública

| Ambiente | Referência | Estado em 2026-09-21 |
| --- | --- | --- |
| Hugging Face Spaces | URL do Space | Pendente |
| GitHub Actions | [`tests/github/workflows/ci.yml`](tests/github/workflows/ci.yml) | Configurado |
| Vídeo de 3-5 min | A definir | Pendente |

## Dívida técnica aceita

Esta etapa não fecha os seguintes pontos:

1. Scheduler do HubSpot desligado; a execução é manual.
2. APIs ainda dependem de contas pessoais e precisam migrar para a conta corporativa.
3. O fluxo real não tem tratamento completo de erro, retry ou alerta no Slack.
4. Não há instrumentação de tokens nem `cost_usd` por lead.
5. Não há mapa jurídico concluído para a transferência internacional de dados.
6. O schema do Airtable permite duplicidade de `deal_id`, tem `tech_stack` como
   *Multiple select* e armazena resultados de busca pesados.
7. Looker, Slack e outras integrações ainda não foram implementados.

Detalhes e ordem de urgência estão em [`docs/notas-joana.md`](docs/notas-joana.md)
e no checklist [`docs/o-que-precisa-construir.md`](docs/o-que-precisa-construir.md).

## Handoff original

O cenário nasceu no espaço pessoal da Joana (`joana@vendemais.com`). O Make não
migra workspaces: a conta corporativa precisa importar o blueprint e recriar as
conexões OAuth/PAT manualmente. As capturas descritas estão em
`docs/cenario-make-screenshots/` e o pseudo-blueprint está em
`make-blueprint-pseudo.txt`.

Consulte [`BRIEFING.md`](BRIEFING.md) e [`CHANGELOG.md`](CHANGELOG.md) para o
contexto histórico do projeto.
