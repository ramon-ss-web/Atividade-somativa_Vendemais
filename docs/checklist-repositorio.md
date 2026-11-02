# Checklist — repositório GitHub público (Etapa 1)

Repo deve ser **público**. Cada item: `[x]` + URL do arquivo no GitHub.

Legenda: **Obrigatório Autônomo** / Recomendado / Já existia no handoff.

---

## 1. Higiene e segredos

| Item | Nível | Arquivo | OK? |
| ---- | ----- | ------- | --- |
| `.gitignore` cobre `.env`, venv, `.n8n/`, `n8n_data/` | Obrigatório | `.gitignore` (já existe — revisar) | [ ] |
| `.env.example` sem valores reais | Obrigatório | `.env.example` | [ ] |
| Nenhum secret real no histórico recente | Obrigatório | `git log -p` / `git grep` | [ ] |
| Placeholder `sk-EXEMPLO-…` removido **ou** claramente fake + Secrets | Obrigatório | `n8n-mirror/workflows/vendemais-enrich-v0.json` | [ ] |
| LICENSE | Recomendado | `LICENSE` | [ ] |

## 2. Documentação de entrega

| Item | Nível | Arquivo | OK? |
| ---- | ----- | ------- | --- |
| README v1 com 5 seções obrigatórias | Obrigatório | `README.md` (fundir esqueleto) | [ ] |
| Auditoria preenchida | Obrigatório | `docs/auditoria-prototipo.md` | [ ] |
| Matriz com pesos frozen | Obrigatório | `docs/matriz-decisao-stack.md` | [ ] |
| ADR-001 e ADR-002 assinados | Obrigatório | `docs/adr/` | [ ] |
| C4 L1 e L2 (PNG + Mermaid) | Obrigatório | `docs/c4-niveis-1-2.md`, `docs/c4/*.png` | [ ] |
| Plano de testes + evidência rollback | Obrigatório | `docs/plano-testes-rollback.md` + `docs/evidencias/` | [ ] |
| Post-mortem 1 página | Obrigatório | `docs/postmortem-blameless.md` | [ ] |
| Roteiro do vídeo + link unlisted | Obrigatório | `docs/roteiro-demonstracao.md` + URL no README | [ ] |
| Mapa LGPD mínimo (dados sintéticos no demo) | Recomendado | `docs/lgpd-mapa-minimo.md` | [ ] |
| Notas Joana / briefing **preservados** | Obrigatório | `docs/notas-joana.md`, `BRIEFING.md` | [ ] |

## 3. Versionamento SemVer

| Item | Nível | Como | OK? |
| ---- | ----- | ---- | --- |
| `CHANGELOG.md` no padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) + SemVer | Obrigatório | Evoluir o changelog da Joana (`v0.4-handoff` → `0.5.0`) | [ ] |
| Tag Git `v0.5.0` (ou a que você publicar) | Obrigatório | `git tag -a v0.5.0 -m "..."` | [ ] |
| Tag anterior usada no rollback | Obrigatório | `v0.5.0` e `v0.5.1` (ou revert) | [ ] |

Modelo de seção nova no CHANGELOG:

```markdown
## [0.5.0] - 2026-09-21
### Added
- GitHub Actions CI
- Hospedagem pública n8n (HF Spaces)
### Changed
- Segredos saem do JSON do mirror
### Fixed
- (se houver)
### Security
- Remoção do apiKey hardcoded
```

## 4. CI/CD

| Item | Nível | Arquivo | OK? |
| ---- | ----- | ------- | --- |
| Workflow CI | Obrigatório | `.github/workflows/ci.yml` | [ ] |
| Badge no README | Recomendado | `![ci](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)` | [ ] |
| CD para Space **ou** evidência de rebuild amarrada ao SHA | Obrigatório Autônomo | `.github/workflows/deploy-hf.yml` **ou** print no `docs/evidencias/` | [ ] |
| Secrets no GitHub: só os necessários (`HF_TOKEN` se CD) | Obrigatório | Settings → Secrets | [ ] |
| Branch protection leve em `main` (opcional) | Recomendado | Settings → Branches | [ ] |

## 5. Runtime e qualidade

| Item | Nível | Arquivo | OK? |
| ---- | ----- | ------- | --- |
| Compose local intacto | Obrigatório | `n8n-mirror/docker-compose.yml` | [ ] |
| Dockerfile **de publicação** (expõe `0.0.0.0:5678`) | Obrigatório | `n8n-mirror/Dockerfile` | [ ] |
| `requirements.txt` mesmo que vazio + comentário “stdlib” | Recomendado | `requirements.txt` | [ ] |
| Testes passando no Actions | Obrigatório | `tests/` | [ ] |

## 6. URL pública

| Item | OK? | Valor |
| ---- | --- | ----- |
| URL do Space / Render | [ ] | `https://` |
| Endpoint smoke documentado | [ ] | `POST …/webhook/lead-enrich-local` |
| Payload de exemplo no README | [ ] | empresa fictícia |
| Aviso de cold start | [ ] |  |

## 7. O que **não** precisa existir (não perca tempo)

- App Next.js na Vercel
- `docker-compose` de Prometheus
- Terraform
- Transferência real da conta Make da Joana (impossível no curso)

---

## Conferência final (90–100%)

- [ ] Clone em pasta vazia: testes passam.
- [ ] README sozinho explica problema → URL.
- [ ] ADRs citam alternativas **descartadas**.
- [ ] Vídeo 3–5 min cobre URL + Actions + 1 falha honesta.
