# ADR-001 — Escolha da stack do sistema publicado

- **Status:** Aceito
- **Data:** 2026-09-21
- **Decisores:** Ramon (RevOps / aluno AI Factory)
- **Consultado:** Briefing Cláudia Mendes; handoff Joana; matriz `docs/matriz-decisao-stack.md`
- **Formato:** [MADR](https://adr.github.io/madr/)

---

## Contexto

A VendeMais herdou um cenário **Make.com** (Stack C) que enriquece deals em `appointmentscheduled`: busca Google → LLM (GPT pequeno, JSON) → Airtable → `icp_match_score` no HubSpot.

O protótipo **já traz** um espelho n8n (`n8n-mirror/`) porque o Make **não roda local**. A Etapa 1 pede sistema em produção com **custo zero**. Make Starter e chaves pessoais da Joana violam custo/identidade. Reescrever em API Python/LangChain violaria a regra de ouro do curso.

Problema a decidir: **qual stack preserva os 5 passos e ainda permite URL pública, CI e secrets corretos no free tier?**

### Decision drivers (espelham os pesos já frozen)

1. US$ 0.
2. Evoluir dívida, não reescrever.
3. Demo clicável pelo avaliador.
4. Git como fonte da verdade.

---

## Decisão

Adotar **stack híbrida de evolução**, não um greenfield:

| Camada | Escolha | Papel |
| ------ | ------- | ----- |
| Contrato herdado | Blueprint Make versionado em `workflows/` | Artefato de produção narrativa VendeMais; **não** é o runtime do aluno se não houver conta free |
| Runtime publicado | **n8n 2.28.7** + workflows já existentes | Mesmos 5 passos; trigger HTTP (dívida O1 aceita e tornada observável) |
| Qualidade | Python stdlib em `tests/` + GitHub Actions | Impede blueprint “manco” |
| Persistência no demo | Resposta JSON do webhook; Airtable **opcional** (schema herdado) | Evita Neon/Supabase sem necessidade |
| LLM no smoke | Workflow `vendemais-enrich-local.json` (mock) | Zero token |
| LLM “real” (opcional) | Groq ou HF Inference, **mesmo schema JSON** | Só se couber no free; senão documentar como dívida C1 |

**Fora de escopo desta decisão:** Looker, Slack, OAuth HubSpot corporativo, sync bidirecional Make API (podem ser ADR-003+).

---

## Consequências

### Boas

- O avaliador reconhece o **mesmo** pipeline descrito no README da Joana.
- Testes que já existem continuam válidos.
- Segredos podem sair do JSON (`apiKey` hardcoded vira credencial do n8n).
- Dá para cumprir Autônomo sem cartão de crédito.

### Ruins / trade-offs

- Produção “de verdade” da VendeMais continua sendo Make; o Space é **sistema publicado do curso**, não o workspace `joana@vendemais.com`.
- Webhook ≠ poll HubSpot 15 min (dívida O1 **explicitamente aceita**).
- n8n 2.x exige conta owner no primeiro boot; precisa de senha no secret do host.
- Duas fontes de workflow (Make JSON ≠ n8n JSON) podem divergir — CI deve falhar se um dos dois perder o encadeamento de 5 nós.

### Confirmação (como saberemos que a decisão está em vigor)

- [x] README raiz lista as 5 camadas da tabela acima.
- [x] Matriz A tem n8n/HF como 1º com contas justificadas.
- [ ] Nenhum `sk-` real no Git (`git grep -i "sk-"` só encontra o placeholder de exemplo, que será removido ou rotulado).

---

## Alternativas descartadas

### Alt-1 — Make.com Free como único runtime

- **Por que considerou:** é o sistema original.
- **Por que descartou:** URL de produto fraca; ops limitadas; risco de cartão; conexões pessoais; não roda no GitHub Actions de ponta a ponta.

### Alt-2 — Reescrever em FastAPI + Vercel + Neon + OpenAI

- **Por que considerou:** “cheira a produção” para portfólio.
- **Por que descartou:** reescrita; abandono do blueprint; Neon/Vercel não orquestram o cenário Make; viola rubrica.

### Alt-3 — Só Hugging Face Spaces com Gradio (UI sem n8n)

- **Por que considerou:** URL fácil.
- **Por que descartou:** abandona os workflows versionados; avaliador não vê evolução do protótipo.

### Alt-4 — Supabase como CRM

- **Por que considerou:** free tier popular na matriz do enunciado.
- **Por que descartou:** schema Airtable já é a dívida C3/C4; migrar CRM agora é reescrita de dados.

---

## Mais informações

- `docs/matriz-decisao-stack.md`
- `docs/adr/ADR-002-hospedagem-deploy.md`
- `BRIEFING.md`, `docs/notas-joana.md`
