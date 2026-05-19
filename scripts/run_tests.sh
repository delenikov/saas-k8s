#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${1:?Usage: ./scripts/run_tests.sh http://LOAD_BALANCER_URL platform-name}
PLATFORM=${2:?Platform name required: eks or aks}

mkdir -p results

for SIZE in 64 128 256 512 1000; do
  for USERS in 10 50 100 500; do

    OUT="results/${PLATFORM}_size${SIZE}_users${USERS}.json"

    echo "========================================"
    echo "Running:"
    echo "Platform: $PLATFORM"
    echo "Size: $SIZE"
    echo "Users: $USERS"
    echo "========================================"

    BASE_URL="$BASE_URL" \
    SIZE="$SIZE" \
    USERS="$USERS" \
    DURATION="1m" \
    k6 run \
      --summary-export "$OUT" \
      loadtest/test.js

  done
done