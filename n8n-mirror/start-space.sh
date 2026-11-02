#!/bin/sh
# Sobe o webhook offline antes do n8n escutar.
# No Space o disco e efemero: import + publish rodam em todo boot.
# Sem SPACE_HOST, o mesmo script serve para testar a imagem no laptop.
set -eu

if [ -n "${SPACE_HOST:-}" ]; then
  export N8N_PROTOCOL=https
  export N8N_HOST="${SPACE_HOST}"
  export WEBHOOK_URL="https://${SPACE_HOST}/"
  export N8N_EDITOR_BASE_URL="https://${SPACE_HOST}/"
else
  export N8N_PROTOCOL="${N8N_PROTOCOL:-http}"
  export N8N_HOST="${N8N_HOST:-localhost}"
  export WEBHOOK_URL="${WEBHOOK_URL:-http://127.0.0.1:5678/}"
  export N8N_EDITOR_BASE_URL="${N8N_EDITOR_BASE_URL:-http://127.0.0.1:5678/}"
fi

echo "VendeMais webhook base: ${WEBHOOK_URL}"
n8n import:workflow --input=/opt/vendemais/vendemais-enrich-local.json
n8n publish:workflow --id=vendemais-lead-enrich-local
exec n8n start
