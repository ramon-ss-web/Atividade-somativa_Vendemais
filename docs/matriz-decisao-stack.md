# Matriz de decisão de stack — Etapa 1 (custo zero)

**Regra MADR:** pesos definidos **antes** das notas. Não alterar peso depois de pontuar (se alterar, registre em “Mudança de peso” no rodapé — isso derruba a nota Autônomo).

**Data do freeze dos pesos:** 2026-09-21  
**Decisor:** Ramon  
**Restrição dura:** US$ 0,00 (somente free tier). Orçamento VendeMais US$ 50/mês do briefing **não** está disponível para o aluno.

---

## 1. Critérios e pesos (freeze)

| ID | Critério | O que mede | Peso |
| -- | -------- | ---------- | ---: |
| K1 | Custo zero sustentável 30 dias | Cabe em free tier com 1 demo + CI | 25 |
| K2 | Fidelidade à dívida herdada | Reusa os 5 passos / JSON existentes | 25 |
| K3 | URL pública + demo reproduzível | Avaliador abre o link e dispara um lead fake | 15 |
| K4 | Git nativo / CI | Push em `main` valida ou publica | 15 |
| K5 | Segredos fora do código | Secrets do provedor, não JSON | 10 |
| K6 | Superfície LGPD no demo | Dá para rodar só com dados sintéticos | 10 |
| | **Total** | | **100** |

Escala de notas: **0** (inviável), **1** (fraco), **2** (aceitável), **3** (forte no critério).

**Score ponderado** = Σ (nota × peso). Máximo = 3 × 100 = **300**.

---

## 2. Opções consideradas (todas free tier)

Não misturar “opção de orquestração” com “opção de página estática”. São **duas matrizes**: runtime do fluxo vs hospedagem do runtime.

### Matriz A — Orquestração do fluxo (o “sistema”)

| Critério (peso) | A1 Make.com Free | A2 n8n no Hugging Face Spaces (Docker) | A3 n8n no Render Free | A4 só testes Python + mock (sem runtime) |
| --------------- | ---------------: | -------------------------------------: | --------------------: | ---------------------------------------: |
| K1 Custo (25) | 2 — 1k ops/mês; cartão costuma ser exigido | 3 — Space Docker gratuito | 2 — spin-down 15 min mata webhook | 3 — zero infra |
| K2 Fidelidade (25) | 3 — é o artefato original | 3 — `n8n-mirror/` já existe | 3 — mesmo compose | 1 — não é o sistema |
| K3 URL pública (15) | 1 — cenário Make não é URL de produto | 3 — `*.hf.space` + webhook | 2 — URL existe mas dorme | 0 |
| K4 CI (15) | 1 — sync API Make é extra e frágil | 2 — CI valida JSON; deploy HF é manual ou token | 2 — deploy Git nativo | 3 — só CI |
| K5 Secrets (10) | 2 — Connections na UI | 3 — Secrets do Space | 3 — Env do Render | 3 |
| K6 LGPD demo (10) | 1 — tenta CRM real | 3 — webhook sintético | 3 | 3 |
| **Ponderado (preenchido)** | **185** | **280** | **245** | **200** |
| **Ranking** | 4º | **1º — escolha** | 2º | 3º |

Cálculo A2 (referência): (3×25)+(3×25)+(3×15)+(2×15)+(3×10)+(3×10) = 75+75+45+30+30+30 = **280**.

Cálculo A1: (2×25)+(3×25)+(1×15)+(1×15)+(2×10)+(1×10) = 50+75+15+15+20+10 = **185**.

> Ajuste **somente as notas** se sua conta HF/Render se comportar diferente. Não mude os pesos.

### Matriz B — Hospedagem / superfície pública

| Critério (peso) | B1 Hugging Face Spaces (Docker n8n) | B2 Render Web Service | B3 Vercel / Netlify | B4 GitHub Pages | B5 Neon + app própria |
| --------------- | ----------------------------------: | --------------------: | ------------------: | --------------: | --------------------: |
| K1 (25) | 3 | 2 (sleep) | 3 | 3 | 3 (DB free) |
| K2 (25) | 3 (compose/workflow prontos) | 3 | 0 (serverless ≠ n8n) | 0 | 0 (reescreve) |
| K3 (15) | 3 | 2 | 1 (só front) | 1 (só docs) | 2 |
| K4 (15) | 2 | 3 | 3 | 3 | 2 |
| K5 (10) | 3 | 3 | 3 | 1 | 3 |
| K6 (10) | 3 | 3 | 3 | 3 | 2 |
| **Ponderado** | **280** | **245** | **185** | **175** | **175** |
| **Ranking** | **1º** | 2º (fallback) | descartar como runtime | só docs | reescrita — recusar |

Cálculo B3: (3×25)+(0×25)+(1×15)+(3×15)+(3×10)+(3×10) = 75+0+15+45+30+30 = **185**.

### Matriz C — LLM no demo (não é o core da Etapa 1, mas aparece no ADR-001)

| Critério | C1 OpenAI GPT pequeno (herdado) | C2 Groq / HF Inference (free) | C3 Workflow `*-local.json` mock |
| -------- | ------------------------------: | ----------------------------: | ------------------------------: |
| K1 | 1 — cartão / crédito acaba | 3 | 3 |
| K2 | 3 | 2 — mesmo JSON de saída | 2 — mesmos nomes de node |
| K3 | 2 | 2 | 3 — sempre verde |
| **Uso recomendado** | Backlog / se houver crédito free | Opcional no Space | **Smoke test obrigatório** |

**Decisão composta (leve para os ADRs):**

1. Contrato herdado versionado: **blueprint Make** (não apagar).
2. Sistema publicado Etapa 1: **n8n (workflow existente) no Hugging Face Spaces**.
3. Fallback se Space recusar Docker: **Render Free** (aceitar cold start e documentar no ADR-002).
4. Página de docs: **GitHub README + (opcional) GitHub Pages**; **não** usar Vercel como “backend do enrichment”.
5. Dados: **Airtable free** se for mostrar persistência; senão a **resposta do webhook** basta. **Neon/Supabase só se** você adicionar `cost_usd` sem abandonar o fluxo — não é necessário para Autônomo.
6. CI: **GitHub Actions** (repo público = minutos free).

---

## 3. Justificativa de uma frase (colar no vídeo)

> “Não subi o Make para produção na minha conta porque quebra custo zero e identidade; publiquei o mirror n8n que o próprio handoff criou para isso, no Hugging Face Spaces, com CI no GitHub.”

---

## 4. Mudança de peso (proibido no Autônomo, a menos que…)

| Data | Critério | Peso antigo → novo | Motivo | Impacto no ranking |
| ---- | -------- | ------------------ | ------ | ------------------ |
| — | — | — | — | — |
