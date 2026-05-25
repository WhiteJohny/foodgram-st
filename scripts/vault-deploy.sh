#!/usr/bin/env bash
# Vault integration + werf deploy
# Usage: VAULT_ADDR=... VAULT_TOKEN=... ./scripts/vault-deploy.sh [env]
#
# In-cluster (Kubernetes pod): VAULT_TOKEN is obtained automatically via
# Kubernetes auth using the pod's service account JWT.
# Outside cluster: export VAULT_TOKEN before running.

set -euo pipefail

VAULT_ADDR="${VAULT_ADDR:-http://vault.vault.svc.cluster.local:8200}"
VAULT_ROLE="${VAULT_ROLE:-foodgram-role}"
VAULT_SECRET_PATH="${VAULT_SECRET_PATH:-foodgram/data/app}"
DEPLOY_ENV="${1:-production}"
NAMESPACE="${NAMESPACE:-foodgram}"

# ── Step 1: Authenticate with Vault ─────────────────────────────────────────
if [ -z "${VAULT_TOKEN:-}" ]; then
  echo "==> No VAULT_TOKEN found — authenticating via Kubernetes service account..."
  SA_JWT=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  VAULT_TOKEN=$(curl -sf \
    --request POST \
    --data "{\"role\":\"${VAULT_ROLE}\",\"jwt\":\"${SA_JWT}\"}" \
    "${VAULT_ADDR}/v1/auth/kubernetes/login" \
    | jq -r '.auth.client_token')
  echo "==> Vault token obtained."
else
  echo "==> Using pre-set VAULT_TOKEN."
fi
export VAULT_TOKEN

# ── Step 2: Fetch secrets from Vault ────────────────────────────────────────
echo "==> Reading secrets from ${VAULT_ADDR}/v1/${VAULT_SECRET_PATH} ..."
SECRET_JSON=$(curl -sf \
  --header "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/${VAULT_SECRET_PATH}")

DOCKER_USERNAME=$(echo "${SECRET_JSON}" | jq -r '.data.data.DOCKER_USERNAME')
DOCKER_TOKEN=$(echo "${SECRET_JSON}" | jq -r '.data.data.DOCKER_TOKEN')

if [ "${DOCKER_USERNAME}" = "null" ] || [ "${DOCKER_TOKEN}" = "null" ]; then
  echo "ERROR: DOCKER_USERNAME or DOCKER_TOKEN not found in Vault at ${VAULT_SECRET_PATH}" >&2
  exit 1
fi

# ── Step 3: Docker Hub login ─────────────────────────────────────────────────
echo "==> Logging in to Docker Hub as ${DOCKER_USERNAME}..."
echo "${DOCKER_TOKEN}" | docker login --username "${DOCKER_USERNAME}" --password-stdin

# ── Step 4: werf converge ────────────────────────────────────────────────────
echo "==> Running werf converge (env=${DEPLOY_ENV}, namespace=${NAMESPACE})..."
werf converge \
  --repo "docker.io/${DOCKER_USERNAME}/foodgram" \
  --env "${DEPLOY_ENV}" \
  --namespace "${NAMESPACE}" \
  --set "global.namespace=${NAMESPACE}"

echo "==> Deploy complete."
