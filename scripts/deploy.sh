#!/usr/bin/env bash
set -euo pipefail

set -a
# shellcheck disable=SC1091
[ -f .env ] && source .env
set +a

NAMESPACE="${NAMESPACE:-foodgram}"
REPO="${REPO:-docker.io/${DOCKER_USER}/foodgram}"

# ── Vault AppRole auth ───────────────────────────────────────────
if [ -n "${VAULT_ROLE_ID:-}" ] && [ -n "${VAULT_SECRET_ID:-}" ]; then
  echo "==> Authenticating with Vault (AppRole)..."
  VAULT_TOKEN=$(curl -sf \
    --request POST \
    --data "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"${VAULT_SECRET_ID}\"}" \
    "${VAULT_ADDR}/v1/auth/approle/login" \
    | jq -r '.auth.client_token')
  export VAULT_TOKEN

  echo "==> Fetching Docker credentials from Vault..."
  SECRET_JSON=$(curl -sf \
    --header "X-Vault-Token: ${VAULT_TOKEN}" \
    "${VAULT_ADDR}/v1/foodgram/data/app")
  DOCKER_USER=$(echo "${SECRET_JSON}" | jq -r '.data.data.DOCKER_USERNAME')
  DOCKER_PASS=$(echo "${SECRET_JSON}" | jq -r '.data.data.DOCKER_TOKEN')
fi

# ── Namespace ────────────────────────────────────────────────────────────────
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# ── Registry login & deploy ──────────────────────────────────────────────────
werf cr login -u "$DOCKER_USER" -p "$DOCKER_PASS" registry-1.docker.io

werf converge \
    --repo "$REPO" \
    --synchronization :local \
    --env production \
    --namespace "$NAMESPACE" \
    --set global.namespace="$NAMESPACE" \
    --kube-config ~/.kube/config
