# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) · versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.5.0] - 2026-09-21

### Added

- Entrega Etapa 1: auditoria, matriz de stack (pesos frozen), ADR-001/002 (MADR), guia C4, plano de testes/rollback, post-mortem, roteiro do vídeo.
- CI GitHub Actions (`.github/workflows/ci.yml`) rodando `tests/validate_workflows.py` e `tests/test_enrichment_logic.py`.
- `n8n-mirror/Dockerfile` para publicação em Hugging Face Spaces (free tier).
- `docs/publicacao.md` como fonte única de URL/identidade.
- `n8n-mirror/start-space.sh`: em todo boot importa e publica `vendemais-enrich-local.json` (o disco do Space é efêmero).
- Space Docker `Ramonss86/vendemais-lead-enrich` (commit `f5fdfc5`). Runtime não sobe: cota `cpu-basic` da conta é 0.

### Changed

- README raiz fundido com o formato acadêmico (problema, solução, como rodar, arquitetura, URL); handoff da Joana preservado em `<details>`.

### Security

- Smoke público da Etapa 1 usa o workflow **offline** (sem chave). Remoção do `apiKey` de exemplo no JSON v0 permanece item da auditoria (S2) até o deploy.

## [v0.4-handoff] (RevOps, herdando da Joana)
- Reconstruído o **blueprint Make.com importável** (`workflows/vendemais-make-blueprint.json`) a partir do pseudo-blueprint + screenshots. 5 módulos.
- Adicionado **mirror n8n** auto-hospedável (`n8n-mirror/`: docker-compose + workflow + README) para testar o mesmo fluxo localmente.
- Adicionados **testes** (`tests/`): validador estrutural dos 2 JSON + teste de lógica com LLM mockado (prompt + parsing do fit-score).
- Primeiro **versionamento Git** do projeto (antes era tudo clicado no Make).
- `.env.example` e `.gitignore` corrigidos.
- Dívida técnica herdada **documentada** no README (não corrigida — material do curso).

## [v0.3-joana]
- Adicionado módulo HubSpot Update (atualiza score no deal)
- icp_match_score agora visível pros vendedores

## [v0.2-joana]
- Trocado o modelo do LLM por um GPT menor e mais barato

## [v0.1-joana]
- Primeira versão funcional: HubSpot → Search → OpenAI → Airtable
- Sem update do HubSpot ainda
