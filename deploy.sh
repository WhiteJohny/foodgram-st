#!/bin/bash
set -e

# Загружаем переменные для доступа к Vault
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Параметры
RELEASE_NAME="my-foodgram"
NAMESPACE="foodgramh"
CHART_PATH="./foodgram-chart"
VALUES_VAULT="values.vault.yaml"
VALUES_BASE="./foodgram-chart/values.yaml"

# Создаём временный файл для подставленных значений
TMP_VALUES=$(mktemp)

echo "Generating final values with vals..."
# Вызываем vals, подставляем секреты и сохраняем во временный файл
vals eval -f "$VALUES_VAULT" > "$TMP_VALUES"

echo "Deploying $RELEASE_NAME to namespace $NAMESPACE..."
# Запускаем helm upgrade, передавая оба values-файла (обычный и с подставленными секретами)
helm upgrade --install "$RELEASE_NAME" "$CHART_PATH" \
    --namespace "$NAMESPACE" \
    --create-namespace \
    --values "$VALUES_BASE" \
    --values "$TMP_VALUES" \
    --wait \
    --timeout 3m

# Удаляем временный файл
rm "$TMP_VALUES"

echo "Done."
