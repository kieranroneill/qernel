#!/bin/sh

# Public: Creates the users ACL for the Redis configuration.
#
# Environment Variables
#
# REDIS_PASSWORD - The password for the Redis user.
# REDIS_USERNAME - The username for the Redis user.
#
# Examples
#   ./entrypoint.sh
main() {
  set -eu

  : "${REDIS_USERNAME:?REDIS_USERNAME is required}"
  : "${REDIS_PASSWORD:?REDIS_PASSWORD is required}"

  envsubst '${REDIS_USERNAME} ${REDIS_PASSWORD}' \
    < /usr/local/etc/redis/users.acl.template \
    > /usr/local/etc/redis/users.acl

  exec "$@"
}

# and so, it begins...
main "$@"
