#!/bin/sh

set -e

ERROR_PREFIX="\033[0;31m[ERROR]\033[0m"
INFO_PREFIX="\033[1;33m[INFO]\033[0m"

# Public: Runs upgrades and starts the API.
#
# Examples
#   ./entrypoint.sh
main() {
  printf "%b running migrations...\n" "$INFO_PREFIX"
  alembic upgrade head

  printf "%b starting api...\n" "$INFO_PREFIX"
  exec python -m api.main
}

# and so, it begins...
main
