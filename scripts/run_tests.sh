#!/bin/bash

set -e

MARKER=$1        # unit | integration | contract | saga | chaos | all
DOMAIN=$2        # optional: products, orders, payments

if [ -z "$MARKER" ]; then
  echo "❌ Usage: ./scripts/run_tests.sh <marker|all> [domain]"
  exit 1
fi

TEST_PATH="core/domains"

if [ -n "$DOMAIN" ]; then
  TEST_PATH="$TEST_PATH/$DOMAIN"
fi

echo "🧪 Running tests"
echo "📌 Marker: $MARKER"
echo "📂 Path: $TEST_PATH"
echo "-----------------------------------"

if [ "$MARKER" = "all" ]; then
  pytest $TEST_PATH -vv
else
  pytest $TEST_PATH -m "$MARKER" -vv
fi
