# Publicação do n8n (Etapa 1). NÃO use o bind 127.0.0.1 do compose local.
# Hugging Face Spaces: este arquivo na raiz do Space + README do Space.
# Imagem pinada — mesma dívida/decisão do docker-compose.yml (não use :latest).
FROM n8nio/n8n:2.28.7

USER root
COPY workflows/vendemais-enrich-local.json /opt/vendemais/vendemais-enrich-local.json
COPY start-space.sh /opt/vendemais/start-space.sh
RUN chmod 755 /opt/vendemais/start-space.sh \
    && chown -R node:node /opt/vendemais
USER node

ENV N8N_PORT=5678 \
    GENERIC_TIMEZONE=America/Sao_Paulo \
    N8N_DIAGNOSTICS_ENABLED=false \
    N8N_PERSONALIZATION_ENABLED=false \
    N8N_PROXY_HOPS=1 \
    N8N_SECURE_COOKIE=false \
    N8N_ENCRYPTION_KEY=vendemais-etapa1-offline-demo

EXPOSE 5678

# WEBHOOK_URL é montada em start-space.sh (SPACE_HOST no HF; localhost no teste da imagem).
ENTRYPOINT ["/opt/vendemais/start-space.sh"]
