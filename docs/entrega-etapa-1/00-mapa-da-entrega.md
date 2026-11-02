# Mapa da entrega — Etapa 1 (nível Autônomo)

Projeto herdado: **VendeMais Lead Enrichment** (cenário Make.com + mirror n8n).
Regra de ouro: **aceitar e evoluir a dívida técnica**, sem reescrever o fluxo HubSpot → Google → LLM → Airtable → HubSpot.

| Parte | Artefato | Arquivo | Status para 90–100% |
| ----- | -------- | ------- | ------------------- |
| 1 | Auditoria do protótipo | [`../auditoria-prototipo.md`](../auditoria-prototipo.md) | Ramon · 2026-09-21 · veredito parcial até URL |
| 1 | Matriz de decisão | [`../matriz-decisao-stack.md`](../matriz-decisao-stack.md) | Pesos frozen 2026-09-21; n8n/HF 1º |
| 1 | ADR-001 Stack | [`../adr/ADR-001-stack.md`](../adr/ADR-001-stack.md) | Assinado Ramon / 2026-09-21 |
| 1 | ADR-002 Hospedagem | [`../adr/ADR-002-hospedagem-deploy.md`](../adr/ADR-002-hospedagem-deploy.md) | Assinado; URL ainda em `publicacao.md` |
| 1 | C4 Níveis 1 e 2 | [`../c4-niveis-1-2.md`](../c4-niveis-1-2.md) | Exportar PNG do Excalidraw **e** manter Mermaid no repo |
| 2 | Checklist do repositório | [`../checklist-repositorio.md`](../checklist-repositorio.md) | Marcar cada item com link |
| 2 | README v1 | [`../README.md`](../../README.md) | **Fundido** em 2026-09-21 (Joana em `<details>`) |
| 2 | Testes e rollback | [`../plano-testes-rollback.md`](../plano-testes-rollback.md) | 3 smokes + 1 rollback com evidência |
| 2 | Post-mortem | [`../postmortem-blameless.md`](../postmortem-blameless.md) | Incidente simulado, 1 página |
| 3 | Roteiro do vídeo | [`../roteiro-demonstracao.md`](../roteiro-demonstracao.md) | Gravar 3–5 min seguindo o timing |

**O que o avaliador precisa ver em 30 segundos:** URL pública viva, GitHub Actions verde, ADRs com alternativa descartada, C4 L1+L2, e uma frase honesta do que ainda é dívida (não fingir que o Make corporativo já está migrado se não estiver).
