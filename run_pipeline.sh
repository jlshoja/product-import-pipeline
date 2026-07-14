#!/usr/bin/env bash
# Bash wrapper to run the automatic pipeline with safe defaults
# Usage: ./run_pipeline.sh [timeout_seconds] [subprocess_retries] [--no-resume]

TIMEOUT=${1:-3600}
RETRIES=${2:-1}
NORESUME=${3:-}

if [ "$NORESUME" = "--no-resume" ] || [ "$NORESUME" = "no-resume" ]; then
  unset AUTO_RESUME
  echo "AUTO_RESUME disabled (will prompt if previous run incomplete)"
else
  export AUTO_RESUME=1
  echo "AUTO_RESUME=1 (will resume previous incomplete runs)"
fi

export PROCESS_TIMEOUT=$TIMEOUT
export PROCESS_SUBPROCESS_RETRY=$RETRIES

echo "PROCESS_TIMEOUT=$PROCESS_TIMEOUT"
echo "PROCESS_SUBPROCESS_RETRY=$PROCESS_SUBPROCESS_RETRY"

python product_extraction/main.py auto
