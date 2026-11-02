# Auditoria do protótipo — VendeMais Lead Enrichment

| Campo | Preencher |
| ----- | --------- |
| Auditor | Ramon |
| Data | 2026-09-21 |
| Escopo | Código nesta pasta + notas da Joana + briefing da Cláudia |
| Versão auditada | `v0.4-handoff` (`CHANGELOG.md`) |
| Método | Leitura do repo + inspeção dos JSON + execução local dos testes (sem API paga) |
| Decisão de evolução | **Não reescrever.** Tratar Make como contrato herdado; publicar o **mirror n8n** como sistema observável de Etapa 1 (free tier). |

---

## 1. Inventário do que existe (não inventar componente)

| Ativo | Caminho | Papel hoje | Roda sozinho? |
| ----- | ------- | ---------- | ------------- |
| Cenário Make (produção narrativa) | `workflows/vendemais-make-blueprint.json` | 5 módulos: HubSpot Watch → Google CSE → OpenAI → Airtable → HubSpot Update | Não. `scheduling.status = off` |
| Pseudo-blueprint | `make-blueprint-pseudo.txt` | Fonte da reconstrução | N/A |
| Mirror n8n “real” | `n8n-mirror/workflows/vendemais-enrich-v0.json` | Mesmos 5 passos; webhook em vez de poll HubSpot | `active: false` (confirmar no JSON) |
| Mirror n8n offline | `n8n-mirror/workflows/vendemais-enrich-local.json` | Code nodes mockados; zero custo | Sim, local |
| Compose | `n8n-mirror/docker-compose.yml` | n8n `2.28.7` só em `127.0.0.1:5678` | Local |
| Testes | `tests/validate_workflows.py`, `tests/test_enrichment_logic.py` | Estrutura JSON + prompt/score mockado | Sim, sem rede |
| Schema | `docs/airtable-schema.md` | Tabela `Lead Enrichment` | Base corporativa (ID placeholder) |
| Secrets template | `.env.example` | Make API + n8n | Sem `.env` versionado (bom) |
| CI/CD | `.github/workflows/ci.yml` | Valida JSON + lógica mock | Sim no YAML; verde no GitHub só depois do push (ver `docs/publicacao.md`) |

---

## 2. Lacunas por categoria

Use **Severidade** Crítica / Alta / Média / Baixa. **Evidência** = arquivo + trecho. **Evolução (não reescrita)** = o que você vai fazer na Etapa 1 vs o que fica como dívida explícita.

### 2.1 Segredos e identidade

| ID | Lacuna | Evidência (preencher linha/print) | Severidade | Evolução Etapa 1 |
| -- | ------ | --------------------------------- | ---------- | ---------------- |
| S1 | Conexões Make apontam para contas **pessoais** da Joana (HubSpot, Google, OpenAI, Airtable) | Blueprint: labels `Joana … Personal`; `__IMTCONN__: 0` | Crítica | Não commitar chave. Documentar migração; no público usar **GitHub Secrets / HF Secrets**. Make corporativo fica backlog se não houver conta free. |
| S2 | API key **hardcoded** no mirror n8n (anti-padrão demonstrado) | `n8n-mirror/workflows/vendemais-enrich-v0.json` campo `apiKey`: `sk-EXEMPLO-PESSOAL-JOANA-…` | Crítica | Remover do JSON publicado; node OpenAI via credencial do n8n. Manter menção no ADR como dívida herdada. |
| S3 | Google CSE `cx` e `key` no JSON | `cx` `017576662512468239146:omuauf_lfve`; `key` `COLOQUE_GOOGLE_CSE_KEY_AQUI` | Alta | Variável de ambiente; CSE próprio (quota 100/dia free) **ou** mock no fluxo público. |
| S4 | `.env.example` lista `GITHUB_TOKEN` — risco de aluno commitar PAT | `.env.example` | Média | Usar `GITHUB_TOKEN` nativo do Actions; PAT só se sync Make exigir, como secret. |

_Sua evidência extra:_ _print do n8n mostrando credencial no cofre, não no node._

### 2.2 Operação e confiabilidade

| ID | Lacuna | Evidência | Severidade | Evolução Etapa 1 |
| -- | ------ | --------- | ---------- | ---------------- |
| O1 | Scheduler OFF; execução manual (“Run once” / curl) | README; `scheduling.status: off`; n8n `active: false` | Crítica | Ativar **um** trigger público (webhook n8n) no free tier. Não fingir poll HubSpot 15 min se a conta HubSpot não for sua. |
| O2 | Zero tratamento de erro; JSON quebrado mata o cenário | `docs/notas-joana.md`; teste `mock_llm_broken` | Alta | No n8n: Error Workflow **ou** ramo `IF` + status `failed`. No Make: deixar como dívida documentada se não for o runtime público. |
| O3 | Sem retry / alerta Slack RevOps | `docs/o-que-precisa-construir.md` item 5 | Alta | Etapa 1: log da execução n8n + falha visível no Actions. Slack = backlog (exige workspace). |
| O4 | Sem deduplicação por `deal_id` | Notas Joana; schema Airtable | Média | Smoke test com mesmo `deal_id` duas vezes; registrar comportamento. Unique constraint = evolução posterior. |
| O5 | Imagem Docker pinada (bom) mas bind só localhost | `docker-compose.yml` | Média | Compose local permanece; produção = compose/Dockerfile no host free (ver ADR-002). |

### 2.3 Custo, prompt e dados

| ID | Lacuna | Evidência | Severidade | Evolução Etapa 1 |
| -- | ------ | --------- | ---------- | ---------------- |
| C1 | Snippets Google **não truncados** → até ~8k tokens | Notas Joana; note no node CSE do n8n | Alta | Já existe `max_snippet=500` em `tests/test_enrichment_logic.py` — **promover** isso ao workflow, não reescrever o LLM. |
| C2 | Sem `cost_usd` / tokens | Schema Airtable | Média | Campo opcional **ou** log `prompt_tokens` no JSON de resposta do webhook. Dashboard Looker = etapa posterior. |
| C3 | `tech_stack` multiple select explode opções | `docs/airtable-schema.md` | Média | No público: gravar como texto/JSON. Não migrar base inteira (seria reescrita). |
| C4 | `raw_search_results` ~80% da quota | Schema | Média | Não persistir raw no demo público; truncar. |

### 2.4 Engenharia e entrega

| ID | Lacuna | Evidência | Severidade | Evolução Etapa 1 |
| -- | ------ | --------- | ---------- | ---------------- |
| E1 | Versionamento Git é recente; Make era só clique | README “Sem versionamento Git originalmente” | Alta | Repo público + CHANGELOG SemVer + tags `v0.5.0+` |
| E2 | Sem CI/CD | Pasta `.github/` inexistente | Crítica | Actions: lint JSON + `python tests/*.py` em todo PR/push |
| E3 | Sem `requirements.txt` / runtime Python pinado | Testes são scripts stdlib — OK, mas não declarado | Média | `requirements.txt` vazio+comentário **ou** `python:3.12` no workflow |
| E4 | README é handoff da Joana, não entrega acadêmica | `README.md` | Alta | Fundir com esqueleto v1 (problema, solução, run, arquitetura, URL) |
| E5 | Sem diagrama C4 / ADR | — | Alta | Este pacote `docs/` |
| E6 | Testes não cobrem o workflow `*-local.json` no validador | `validate_workflows.py` só v0 | Média | Estender validador (evolução pequena) |
| E7 | Sem LICENSE visível na entrega do aluno se for fork | `LICENSE` MIT do material do curso | Baixa | Manter MIT; citar origem |

### 2.5 Conformidade (LGPD) — não “resolver jurídico”, mapear

| ID | Lacuna | Evidência | Severidade | Evolução Etapa 1 |
| -- | ------ | --------- | ---------- | ---------------- |
| L1 | Transferência internacional Google + OpenAI (EUA) sem DPA visível | Briefing Cláudia; notas Joana | Alta | Página `docs/lgpd-mapa-minimo.md` (base legal B2B, categorias de dado = **empresa**, não CPF). Demo público só com **empresa fictícia**. |
| L2 | Base ID Airtable placeholder | `appXXXXXXXXXX` | Média | Demo: não usar CRM real de cliente. |

---

## 3. O que **não** entra na Etapa 1 (dívida aceita)

Escreva em 5 linhas o contrato com o avaliador:

1. _Não_ recriar o produto em FastAPI/LangChain.
2. _Não_ exigir HubSpot admin da VendeMais de verdade (usar payload sintético no webhook).
3. _Não_ ligar scheduler Make na conta pessoal da Joana.
4. _Não_ dashboard Looker completo (só plano + 1 view se der tempo).
5. _Não_ pitch de 20 min do comitê (é outra semana do curso).

---

## 4. Riscos se eu “reescrever do zero” (anti-padrão da rubrica)

- Perder o contrato dos 5 módulos que o time RevOps já usa.
- Avaliador marca como **não cumpriu regra de ouro**.
- Introduzir stack nova sem ADR.

---

## 5. Veredito (preencher no fim da auditoria)

| Pergunta | Sim/Não | Comentário |
| -------- | ------- | ---------- |
| Consigo publicar uma URL que executa o **mesmo** encadeamento de 5 passos? | Parcial | Encadeamento existe no n8n local (`lead-enrich-local`). URL HTTPS ainda PENDENTE em `docs/publicacao.md`. |
| Segredos saíram do Git? | Parcial | Smoke não usa chave. O JSON v0 ainda contém `sk-EXEMPLO-…` (S2 — anti-padrão herdado, remover antes do push público se o avaliador fizer `git grep`). |
| CI quebra se o blueprint perder um módulo? | Sim (local) | `validate_workflows.py` + workflow Actions. Confirmar run verde após o primeiro push. |
| C4 L1 e L2 batem com o deploy real? | Parcial | Mermaid no repo. PNG Excalidraw + URL do Space ainda faltam. |

**Veredito:** Pronto para **fechar documentação**; **bloqueado para nota Autônomo completa** até existir URL em `docs/publicacao.md` + evidências de smoke/rollback.
