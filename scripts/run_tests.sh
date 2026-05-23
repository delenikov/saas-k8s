#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${1:?Usage: ./scripts/run_tests.sh http://LOAD_BALANCER_URL platform-name}
PLATFORM=${2:?Platform name required: eks or aks}

mkdir -p results

TEST_CASES=(
  "TC1 10 1"
  "TC2 10 5"
  "TC3 10 10"
  "TC4 10 25"
  "TC5 10 50"
  "TC6 10 100"

  "TC7 25 1"
  "TC8 25 5"
  "TC9 25 10"
  "TC10 25 25"
  "TC11 25 50"
  "TC12 25 100"

  "TC13 50 1"
  "TC14 50 5"
  "TC15 50 10"
  "TC16 50 25"
  "TC17 50 50"
  "TC18 50 100"

  "TC19 100 1"
  "TC20 100 5"
  "TC21 100 10"
  "TC22 100 25"
  "TC23 100 50"
  "TC24 100 100"

  "TC25 250 1"
  "TC26 250 5"
  "TC27 250 10"
  "TC28 250 25"
  "TC29 250 50"
  "TC30 250 100"

  "TC31 350 1"
  "TC32 350 5"
  "TC33 350 10"
  "TC34 350 25"
  "TC35 350 50"
  "TC36 350 100"

  "TC37 500 1"
  "TC38 500 5"
  "TC39 500 10"
  "TC40 500 25"
  "TC41 500 50"
  "TC42 500 100"
)

for TEST in "${TEST_CASES[@]}"; do

  read NAME SIZE USERS <<< "$TEST"

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