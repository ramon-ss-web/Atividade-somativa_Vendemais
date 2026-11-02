# Roteiro de vídeo — 3 a 5 minutos (Etapa 1)

**Formato:** você fala + tela cheia. Resolução 1080p. Sem trilha alta. Link **unlisted** no README.  
**Não mostre:** `.env`, Secrets do GitHub abertos, senha do n8n, dados reais de cliente.

Cronômetro alvo: **4:00**. Se passar de 5:00, corte a seção 5.

---

## 0:00–0:25 — Abertura (câmera ou só tela com seu nome)

Falar:

> “Sou Ramon, Etapa 1 do AI Factory. Herdei o Lead Enrichment da VendeMais — Make.com da Joana, scheduler off e chave pessoal. A regra foi evoluir, não reescrever. Vou mostrar a URL pública do mesmo fluxo de 5 passos, o CI no GitHub Actions, e um rollback.”

Mostrar: README no GitHub já com a URL (zoom no topo).

---

## 0:25–1:20 — URL pública (SMOKE-02)

**Tela:** terminal + aba do Space.

1. Abrir a URL de `docs/publicacao.md` (se pedir login do n8n, **não** digite senha na gravação — mostre só a landing ou vá direto ao curl).  
2. Se hibernou: “cold start de free tier, ADR-002”. Espere 1 hit.  
3. Rodar o `curl` do README **na íntegra**.  
4. Destacar no JSON: `deal_id`, `company` fictícia, `icp_match_score`.  
5. Uma frase: “Isso é o workflow `lead-enrich-local`, mock, custo zero. O blueprint Make continua no Git como contrato da VendeMais.”

**Se der 502:** narre o retry uma vez. Se persistir, **não improvise 2 minutos** — vá para Actions e declare o incidente (isso casa com o post-mortem). Melhor honesto do que fingir.

---

## 1:20–2:35 — Disparo do deploy via GitHub Actions

**Tela:** GitHub → Actions.

Roteiro de fala:

> “Fonte da verdade é o Git. Todo push em main roda `validate_workflows.py` e o teste de lógica com LLM mockado.”

Passos para **mostrar ao vivo** (prepare a branch antes):

1. Abrir `.github/workflows/ci.yml` 5 segundos (não ler YAML linha a linha).  
2. Mostrar o **último run verde** (SMOKE-01).  
3. **Disparo:** um commit trivial visível — por exemplo alterar uma linha do CHANGELOG `docs: ping demo` **ou** o fluxo do SMOKE-03 em branch.  
   - Autônomo de verdade: faça push e **espere o amarelo virar verde** na gravação.  
   - Se a rede estiver lenta: tenha um run de 10 min atrás e diga “este é o pipeline que acabei de disparar”, mostrando o timestamp.  
4. Se tiver CD: job `deploy` / rebuild HF. Se CD for manual: clique Rebuild no Space e mostre o SHA do commit no card do Space.

Frase de ouro:

> “O Make não está no meu cartão. O Actions não publica o cenário da Joana; ele **impede** o JSON de perder os 5 módulos e replica o n8n no Space.”

---

## 2:35–3:35 — O que deu certo e o que deu errado

Fale em **duas colunas** (pode abrir a auditoria 3s):

**Certo**

- 5 passos preservados  
- Segredo hardcoded identificado e tirado do caminho de prod  
- URL + CI + tag SemVer  

**Errado / dívida aceita** (obrigatório para Autônomo — avaliador pune “está perfeito”)

- Poll HubSpot continua OFF (webhook no lugar)  
- Sem Slack, sem `cost_usd`, sem DPA  
- Free tier hiberna  
- Make e n8n podem divergir  

Mostre 5s do **SMOKE-03 vermelho** (CI falhando de propósito) e o verde seguinte: “pipeline não é enfeite”.

---

## 3:35–4:20 — Rollback (evidência)

**Tela:** `docs/plano-testes-rollback.md` preenchido + dois curls.

1. “Versão ruim: webhook 404.” Print **já na pasta evidências** se não quiser quebrar a demo ao vivo.  
2. `git log --oneline -5` mostrando `Revert`.  
3. Curl de novo → 200.  
4. “Post-mortem blameless: causa é contrato HTTP sem probe no CD, não ‘alguém clicou errado’.”

---

## 4:20–4:45 — Encerramento

> “Próximo: error branch no fluxo e truncar snippet (já está no teste Python). Obrigado.”

Cortar.

---

## Lista de janelas para ter abertas *antes* de gravar

1. README GitHub  
2. Terminal com `curl` pronto (seta para cima)  
3. Actions  
4. Pasta `docs/evidencias/`  
5. ADR-001 título (opcional 3s)

## O que **não** falar

- “Reescrevi em LangChain.”  
- “Está 100% igual à produção da Cláudia.”  
- Preço de GPU / Fine-tune.

## Take extra (se o professor pedir 5:00 cheios)

10s do C4 L1 no Excalidraw: “AE, HubSpot, sistema, Google, LLM, Airtable.”
