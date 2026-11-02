# Plano de testes e rollback — Etapa 1

**Sistema sob teste:** n8n publicado (HF Space) + CI GitHub + workflows versionados.  
**Fora de escopo:** conta Make da Joana, HubSpot real da VendeMais.

Preencha a coluna Evidência com **link** (run do Actions, gist, PNG em `docs/evidencias/`).

---

## 1. Três smoke tests (modelo)

Definição: teste **rápido**, ponta a ponta do que o avaliador vê, sem suíte enorme. Se um falhar, **não grave o vídeo ainda**.

### Smoke 1 — Contrato dos workflows (CI)

| Campo | Conteúdo |
| ----- | -------- |
| ID | SMOKE-01 |
| Objetivo | Garantir que Make blueprint e n8n v0 ainda têm ≥ 5 passos encadeados |
| Pré-condição | Repo clonado; Python 3.10+ |
| Passos | 1. `python tests/validate_workflows.py` 2. Conferir exit code 0 no Actions em `main` |
| Dado | Arquivos JSON do repo (sem rede) |
| Esperado | `RESULTADO: todas as verificacoes passaram.` Badge CI verde |
| Evidência | URL do run: colar de `{GitHub}/actions` depois do push (`docs/publicacao.md`) |
| Última execução | 2026-09-21 · pendente (rodar `python tests/validate_workflows.py` e colar pass/fail) |

### Smoke 2 — Enrichment mock na URL pública (demo $0)

| Campo | Conteúdo |
| ----- | -------- |
| ID | SMOKE-02 |
| Objetivo | Avaliador dispara um lead **fictício** e recebe JSON com score |
| Pré-condição | Space acordado (1 hit de aquecimento se hibernar) |
| Passos | 1. `curl -i -X POST "$URL/webhook/lead-enrich-local" -H "Content-Type: application/json" -d '{"deal_id":"9876543210","company":"Acme Logística SA"}'` 2. Salvar body em `docs/evidencias/smoke-02-response.json` |
| Dado | `deal_id=9876543210` (determinístico no mock) |
| Esperado | HTTP 200; `status`/`icp_match_score` presentes; score **60** no fluxo local documentado pela Joana |
| Evidência | JSON + print da execução no n8n (Executions) — pasta `docs/evidencias/` |
| Última execução | pendente · URL ainda PENDENTE em `docs/publicacao.md` (até lá, o mesmo curl em `localhost:5678`) |

### Smoke 3 — Pipeline quebra quando o contrato quebra (regressão)

| Campo | Conteúdo |
| ----- | -------- |
| ID | SMOKE-03 |
| Objetivo | Mostrar que o CI **pega** dívida/regressão — não é badge cosmética |
| Pré-condição | Branch `test/smoke-03-ci-fail` (não mergear) |
| Passos | 1. Remover **temporariamente** 1 módulo do `flow` no blueprint (cópia na branch) 2. Push 3. Actions **red** 4. Reverter commit / fechar PR 5. `main` volta a verde |
| Dado | Diff mínimo no JSON |
| Esperado | Job fail em `validate_workflows.py`; PR não entra em `main` |
| Evidência | Print vermelho + print verde depois. URLs dos dois runs |
| Última execução | pendente · exige GitHub remoto |

> SMOKE-03 é o que separa “Autônomo” de “subi um YAML”. Grave 20s disso no vídeo.

Teste de lógica extra (não conta como um dos 3, mas rode): `python tests/test_enrichment_logic.py` (JSON quebrado do LLM).

---

## 2. Rollback executado com sucesso — passo a passo de evidência

Objetivo da rubrica: **provar** que você sabe voltar, não só avançar.

### 2.1 Preparar duas versões (antes do “incidente”)

1. Tag estável: `v0.5.0` = smoke 02 verde.  
2. Tag “ruim”: `v0.5.1-bad` **ou** commit na `main` que quebra de propósito algo **visível** (ex.: path do webhook errado `lead-enrich-local-typo`, ou mensagem `status: "broken-on-purpose"` no Code node).  
3. Publicar a versão ruim no Space (rebuild).  
4. Rodar o mesmo `curl` do SMOKE-02 → **falha** (404 ou JSON errado).  
   Salvar: `docs/evidencias/rollback-01-antes.png` (terminal) + `rollback-01-actions-bad.png`.

### 2.2 Executar o rollback (escolha um método e **não misture** na evidência)

**Método A — `git revert` (preferível, histórico honesto)**

```text
git checkout main
git pull
git revert --no-edit <SHA_DO_COMMIT_RUIM>
git push origin main
# tag
git tag -a v0.5.2-rollback -m "rollback: restaura webhook smoke"
git push origin v0.5.2-rollback
```

Rebuild do Space no SHA do revert (Actions CD **ou** botão Rebuild + conferir SHA).

**Método B — redeploy da tag boa**

No Space: checkout `v0.5.0` / pin da imagem / “Restore previous revision” do HF. Registrar qual UI você usou.

**Não use** `git push --force` na `main` para a entrega (apaga evidência).

### 2.3 Provar que voltou

1. Mesmo `curl` do SMOKE-02 → 200 e score 60.  
2. Actions da `main` verde no SHA do revert.  
3. Preencher a ata abaixo.

### 2.4 Ata de rollback (cole no PDF/página da entrega)

| Campo | Valor |
| ----- | ----- |
| Incidente simulado | path do webhook quebrado na tag `v0.5.1-bad` (drill) |
| Detectado por | SMOKE-02 (preencher hh:mm UTC-3 no drill) |
| Versão ruim | SHA / tag a colar no drill |
| Versão restaurada | SHA / tag `v0.5.2-rollback` |
| Método | `git revert` (preferível) |
| Tempo até recuperar | meta: ≤ 15 min |
| Comando curl “antes” | anexo `rollback-01-antes.png` |
| Comando curl “depois” | anexo `rollback-02-depois.png` |
| Run CI ruim | URL |
| Run CI bom | URL |
| Revisão HF/Render | print da revision |
| Quem executou | Ramon |
| Data | preencher no drill |

**Critério de sucesso:** terceira pessoa consegue, só com esta ata + anexos, repetir a história sem assistir o vídeo.

---

## 3. Pasta de evidências (crie)

```
docs/evidencias/
  smoke-01-actions.png
  smoke-02-response.json
  smoke-03-red.png
  smoke-03-green.png
  rollback-01-antes.png
  rollback-02-depois.png
  rollback-ata.md    # pode ser esta seção copiada preenchida
```

Não commitar dumps com PII. Só **Acme Logística SA**.
