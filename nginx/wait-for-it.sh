#!/usr/bin/env sh
# wait-for-it.sh: Wait until the given HTTP endpoints respond with 200..399
# Usage: ./wait-for-it.sh URL1 URL2 -- command to execute

set -e
TIMEOUT=60

# Collect URLs until we see --
URLS=""
while [ $# -gt 0 ]; do
  if [ "$1" = "--" ]; then shift; break; fi
  URLS="$URLS $1"
  shift
done

for URL in $URLS; do
  echo "Waiting for $URL ..."
  start_time=$(date +%s)
  while : ; do
    if curl -s -o /dev/null -w "%{http_code}" "$URL" | grep -E "2..|3.." >/dev/null; then
      echo "$URL is up"
      break
    fi
    now=$(date +%s)
    if [ $((now - start_time)) -ge $TIMEOUT ]; then
      echo "Timeout waiting for $URL" >&2
      exit 1
    fi
    sleep 2
  done
done

exec "$@"
