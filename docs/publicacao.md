# Identidade da entrega (fonte única)

Edite **só este arquivo** quando o GitHub ou o Space existirem. O README e os ADRs apontam para cá.

| Campo | Valor |
| ----- | ----- |
| Aluno / auditor / decisor | Ramon |
| Papel | RevOps Specialist (aluno — AI Factory, Etapa 1) |
| Data da auditoria e freeze dos pesos | 2026-09-21 |
| Versão desta entrega | `0.5.0` |
| Tag Git prevista | `v0.5.0` |
| Contrato herdado | `v0.4-handoff` (Joana) |
| Runtime publicado (decisão ADR-002) | n8n `2.28.7` no Hugging Face Spaces (Docker) |
| Fallback | Render Free (cold start) |
| Path do smoke (obrigatório, já está no JSON) | `/webhook/lead-enrich-local` |
| Payload canônico | `{"deal_id":"9876543210","company":"Acme Logística SA"}` |
| Score esperado no mock | `60` (determinístico a partir do `deal_id`) |

## Links que dependem de você publicar

Cole o valor real na coluna da direita. Enquanto estiver `PENDENTE`, o avaliador usa o **smoke local** do README.

| Campo | Valor |
| ----- | ----- |
| GitHub (HTTPS) | https://github.com/ramon-ss-web/Atividade-somativa_Vendemais |
| Actions (CI) | https://github.com/ramon-ss-web/Atividade-somativa_Vendemais/actions/workflows/ci.yml |
| Hugging Face Space (app) | PENDENTE — o Space [Ramonss86/Vendemais](https://huggingface.co/spaces/Ramonss86/Vendemais) é SDK **static** (`https://ramonss86-vendemais.static.hf.space`). Não é o n8n Docker. Não usar essa URL no curl. |
| URL pública (webhook) | PENDENTE — só depois do Space Docker (`n8nio/n8n:2.28.7`) publicado |
| SHA publicado no Space | PENDENTE — `git rev-parse --short HEAD` depois do primeiro deploy Docker |
| Vídeo unlisted (3–5 min) | PENDENTE |

**Smoke público (depois de colar a URL):**

```bash
curl -X POST "https://COLE-A-URL-DO-SPACE/webhook/lead-enrich-local" \
  -H "Content-Type: application/json" \
  -d "{\"deal_id\": \"9876543210\", \"company\": \"Acme Logística SA\"}"
```

**Smoke local (já funciona sem conta):** ver README seção B.
