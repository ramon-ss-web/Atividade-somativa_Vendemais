# Post-mortem (blameless) — 1 página

**Incidente simulado (drill — fechar após executar o rollback):** em data a registrar na ata, o smoke da URL pública passou a responder **404** no webhook `lead-enrich-local` após um “ajuste rápido” no JSON do n8n (path alterado / workflow despublicado), durante ~15 minutos, sem alerta.  
Substitua SHA e horários pelos **reais** do drill em `docs/plano-testes-rollback.md`.

| | |
| --- | --- |
| **Severidade** | SEV-2 (demo acadêmica fora do ar; sem impacto em cliente VendeMais real) |
| **Status** | Rascunho até o drill · depois Encerrado |
| **Autores** | Ramon (facilitador) — **sem nomes na causa** |
| **Data do doc** | 2026-09-21 (abrir) / data do drill (fechar) |
| **Sistemas** | n8n no Hugging Face Spaces, GitHub Actions, workflows em Git |

---

## 1. Resumo executivo (5 linhas)

O enrichment publicado deixou de aceitar o POST documentado no README. A detecção foi **manual** (curl do SMOKE-02), não um monitor. A recuperação foi rollback para a tag anterior. Não houve vazamento de dado pessoal (payload sintético). O buraco: **mudança de contrato HTTP sem teste automatizado no deploy** e **runtime que pode hibernar / desativar workflow**.

---

## 2. Linha do tempo (UTC-3)

| Hora | Evento observável | Sinal |
| ---- | ----------------- | ----- |
| _t+0_ | Push / rebuild do Space com workflow inativo ou path novo | SHA a colar após o drill |
| _t+2 min_ | Primeiro `curl` documentado retorna 404/502 | Terminal |
| _t+3 min_ | CI ainda verde *(JSON local passou, host divergiu)* | Actions |
| _t+5 min_ | Decisão: rollback, não “hotfix no editor do n8n” | Aprendizado |
| _t+12 min_ | `git revert` + rebuild | Tag `v0.5.2-rollback` |
| _t+15 min_ | SMOKE-02 200 + score 60 | `docs/evidencias/rollback-02-depois.png` |
| _t+20 min_ | Este post-mortem fechado | |

---

## 3. Impacto

- Avaliador / demo: URL do README mentirosa por _N_ min.  
- VendeMais produção Make: **nenhum** (não era o host).  
- LGPD: nenhum dado de cliente real.  
- Custo: US$ 0.

---

## 4. Causa-raiz **sistêmica** (5 Whys — sem culpados)

Não escreva “eu esqueci” como causa final.

1. Por que o webhook 404? → O runtime não tinha o path publicado.  
2. Por que o path divergiu do README? → Contrato HTTP vive em **dois lugares** (JSON n8n + README) sem checagem.  
3. Por que o CI não pegou? → CI valida estrutura interna, **não** o HTTP do Space.  
4. Por que ninguém foi alertado? → Não existe probe sintético periódico (cron gratuito limitado).  
5. Por que o editor do n8n permitiu drift vs Git? → Fonte da verdade no host não estava bloqueada (“GitOps frouxo”).

**Causa-raiz:** ausência de **teste de contrato contra a URL de produção** no pipeline e permissão de drift UI vs Git.  
**Não é causa-raiz:** “pessoa X é desatenta”.

Condições que ajudaram (dívida herdada, aceita): scheduler OFF no Make; workflow `active: false` no JSON original; hibernação de free tier.

---

## 5. O que correu bem

- Smoke documentado existia — falha foi **detectável**.  
- Revert em Git preservou história (sem force-push).  
- Payload sintético limitou dano.

---

## 6. Ações concretas (owner + prazo)

| ID | Ação | Owner | Prazo | Feito? |
| -- | ---- | ----- | ----- | ------ |
| A1 | Job no Actions: `curl` no Space após deploy (fail o CD se ≠ 200) | Ramon | 2026-09-24 | [ ] |
| A2 | Um único lugar documenta o path do webhook | Ramon | 2026-09-21 | [x] `docs/publicacao.md` |
| A3 | Desligar edição no Space ou exportar workflow no CI (diff) | Ramon | 2026-09-28 | [ ] |
| A4 | Aviso de cold start + “primeiro 502 não é incidente” no README | Ramon | 2026-09-21 | [x] |
| A5 | Backlog: alerta Slack RevOps (desafio 12 semanas item 5) | RevOps / futuro | fora da Etapa 1 | [ ] |

Se uma ação não tiver owner **nomeado** e data, a rubrica trata como teatro.

---

## 7. Lição para a VendeMais (1 parágrafo)

Sistemas no-code quebram **em silêncio** (Joana: JSON inválido 3×). Publicar o mirror não elimina isso: só torna o silêncio visível se houver smoke na **URL real**. A próxima evolução (tratamento de erro no cenário Make) deve copiar o mesmo contrato de teste, não só “ligar o scheduler”.
