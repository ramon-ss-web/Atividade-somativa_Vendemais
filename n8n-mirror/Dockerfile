# Publicação do n8n (Etapa 1). NÃO use o bind 127.0.0.1 do compose local.
# Hugging Face Spaces: este arquivo na raiz do Space + README do Space.
# Imagem pinada — mesma dívida/decisão do docker-compose.yml (não use :latest).
FROM n8nio/n8n:2.28.7

ENV N8N_PORT=5678 \
    N8N_PROTOCOL=http \
    GENERIC_TIMEZONE=America/Sao_Paulo \
    N8N_DIAGNOSTICS_ENABLED=false \
    N8N_PERSONALIZATION_ENABLED=false

EXPOSE 5678

# WEBHOOK_URL deve ser o HTTPS público do Space (secret/variável do host),
# senão o path do webhook interno não bate com o curl do avaliador.
