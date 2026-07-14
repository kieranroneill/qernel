#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "${0}")

source "${SCRIPT_DIR}/utilities/_set_vars.sh"

# Starts the necessary Docker services and runs integration tests.
#
#
# Examples
#   ./entrypoint.sh
function main {
  _set_vars

  # start the services
  printf "%b starting docker services... \n" "${INFO_PREFIX}"
  docker compose \
	 	-f ./deployments/compose.test.yml \
	 	-p qernel-test \
	 	--env-file .env.test \
		up \
		-d \
		--wait

  # run the integration tests
  printf "%b running integration tests... \n" "${INFO_PREFIX}"
  python3 -m pytest -vv -s --log-cli-level=ERROR test/integration

  # stop the services and remove
  printf "%b shutting down docker services... \n" "${INFO_PREFIX}"
  docker compose \
	 	-f ./deployments/compose.test.yml \
	 	-p qernel-test \
		down
}

# and so, it begins...
main
