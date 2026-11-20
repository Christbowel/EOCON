#!/bin/sh
set -e

BINARY="${1:-./minicalc}"
DURATION="${2:-60}"
CHARSET='0123456789+*/%()\n -'

if [ ! -x "$BINARY" ]; then
    echo "usage: $0 <binary> [duration_seconds]"
    exit 1
fi

echo "dumb fuzzing $BINARY for ${DURATION}s ..."

crashes=0
runs=0
end=$(($(date +%s) + DURATION))

while [ "$(date +%s)" -lt "$end" ]; do
    len=$((RANDOM % 200 + 1))
    input=$(cat /dev/urandom | tr -dc "$CHARSET" | head -c "$len" 2>/dev/null || true)

    echo "$input" | timeout 2 "$BINARY" >/dev/null 2>&1 || {
        code=$?
        if [ "$code" -gt 128 ]; then
            crashes=$((crashes + 1))
        fi
    }

    runs=$((runs + 1))
done

echo "runs: $runs"
echo "crashes: $crashes"
