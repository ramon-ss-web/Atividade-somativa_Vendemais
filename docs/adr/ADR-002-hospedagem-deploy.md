# ADR-002 — Hospedagem e deploy

- **Status:** Aceito
- **Data:** 2026-09-21
- **Decisores:** Ramon
- **Relacionado:** ADR-001 (stack)
- **Formato:** MADR

---

## Contexto

Com a stack travada (n8n + workflows herdados + GitHub Actions), falta decidir **onde** o n8n fica público e **como** um `git push` vira evidência de deploy.

Restrições:

- Free tier apenas.
- `docker-compose.yml` atual **amarra** `127.0.0.1:5678` — correto para laptop, inútil como URL pública.
- Vercel/Netlify são ótimos para front estático e **ruins** para processo longo n8n.
- Render Free **dorme**; o primeiro `curl` do avaliador pode 502.
- Hugging Face Spaces aceita **Docker** e gera `https://<user>-<space>.hf.space`.

Problema: **qual host e qual pipeline de deploy para a Etapa 1?**

---

## Decisão

### Hospedagem primária

**Hugging Face Spaces, SDK Docker**, imagem alinhada a `n8nio/n8n:2.28.7`.

- URL pública: ver tabela em [`docs/publicacao.md`](../publicacao.md). Space Docker criado em 2026-11-02; runtime pausado por cota `cpu-basic` (limit 0) — o webhook ainda não responde.
- Webhook smoke (offline): `POST /webhook/lead-enrich-local`
- Webhook “real” (se houver secrets): `POST /webhook/lead-enrich`
- Variáveis no Space (não no Git): `N8N_BASIC_AUTH` / owner password, `WEBHOOK_URL=https://<space>/`, chaves opcionais.

### Hospedagem de fallback (se Docker no Space falhar na sua conta)

**Render Free** com o mesmo Dockerfile. Documentar cold start de ~50s no README e no vídeo.

### Superfície de documentação

README no GitHub (obrigatório). GitHub Pages **opcional** só para C4 exportado. **Não** declarar Vercel como ambiente do enrichment.

### Deploy automatizado (o que o vídeo precisa mostrar)

1. **CI em todo push/PR** (obrigatório, $0 em repo público):
   - checkout
   - `python tests/validate_workflows.py`
   - `python tests/test_enrichment_logic.py`
2. **CD mínimo Autônomo** — escolha **uma** e registre aqui:
   - **Opção H (recomendada se tiver `HF_TOKEN`):** job `deploy` que faz `huggingface-cli upload` do Dockerfile + workflows **ou** rebuild do Space via API.
   - **Opção M (aceitável):** CI verde + botão **Rebuild** do Space gravado no vídeo; no README, o SHA do commit que está no Space (`git rev-parse --short HEAD`).

**Não** implementar na Etapa 1 o cron “Make puxa blueprint e abre PR” (item 4 do desafio de 12 semanas) — isso é evolução posterior. Mencionar como backlog no CHANGELOG.

### Rollback

Tag Git SemVer + rebuild do Space no commit anterior. Procedimento detalhado em `docs/plano-testes-rollback.md`.

---

## Consequências

### Boas

- URL HTTPS gratuita, alinhada ao enunciado (HF Spaces estava na lista).
- Mesma imagem Docker já testada no curso (`2.28.7`).
- CI bloqueia regressão estrutural sem gastar LLM.

### Ruins

- Space pode hibernar; primeiro hit lento — **avisar no README** (é honesto, não é falha escondida).
- Editor n8n público é risco: **desligar edição** ou proteger com senha forte; preferir webhook-only na demo.
- Dockerfile de produção precisa soltar o bind `127.0.0.1` — mudança **localizada** no compose/Dockerfile, não no algoritmo de enrichment.

### Confirmação

- [ ] `curl` na URL pública devolve JSON com `icp_match_score` para empresa fictícia.
- [ ] Actions: badge no README (YAML já existe; badge depois do remote).
- [ ] Secrets: zero no diff do Git (S2: tirar `sk-EXEMPLO` do JSON v0 antes do push público).
- [x] C4 Nível 2 (Mermaid) mostra HF Space + GitHub Actions, **não** Vercel.

---

## Alternativas descartadas

### Alt-1 — Vercel (serverless)

Timeout, sem processo n8n persistente. Serve no máximo um proxy. Descartado como host do sistema.

### Alt-2 — Somente localhost + ngrok

URL murcha depois da aula. Não é produção da Etapa 1.

### Alt-3 — Fly.io / Railway

Free tier instável ou cartão. Fora da restrição “custo zero confiável”.

### Alt-4 — Make Cloud como URL

Não há endpoint estável de produto para o avaliador; conexões pessoais.

### Alt-5 — Neon/Supabase como host

São banco, não orquestrador. Descartados para ADR-002 (podem aparecer num ADR futuro de `cost_usd`).

---

## Mais informações

- `n8n-mirror/docker-compose.yml`
- `docs/matriz-decisao-stack.md` (Matriz B)
- Plano de rollback
