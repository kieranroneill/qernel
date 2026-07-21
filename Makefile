SHELL := /bin/bash

.PHONY: create_migrations dev start test

all: install

###
# installation
###

install:
	${MAKE} install_js_deps
	${MAKE} install_py_dev_deps
	${MAKE} install_py_deps

install_js_deps:
	@echo ">>> installing javascript dependencies"
	pnpm install

install_py_dev_deps:
	@echo ">>> installing python development dependencies"
	python3 -m venv .venv
	source .venv/bin/activate && \
		pip install -r pip-requirements.txt && \
		pip install -r dev-requirements.txt && \
		deactivate

install_py_deps:
	@echo ">>> installing python dependencies"
	python3 -m venv .venv
	source .venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

###
# docker
###

dev:
	docker compose \
	 	-f ./deployments/compose.development.yml \
	 	-p qernel-dev \
	 	--env-file .env.dev \
	 	--env-file .env.local \
		up \
		--build

start:
	docker compose \
		-f ./deployments/compose.yml \
	 	-p qernel \
		--env-file .env \
		up \
		--build

###
# database
###

database_downgrade:
	docker compose \
		-f ./deployments/compose.yml \
	 	-p qernel \
		run \
		--build \
		--rm api \
		alembic downgrade -1

database_downgrade_dev:
	docker compose \
		-f ./deployments/compose.development.yml \
	 	-p qernel-dev \
		run \
		--build \
		--rm api \
		alembic downgrade -1

database_upgrade:
	docker compose \
		-f ./deployments/compose.yml \
	 	-p qernel \
		run \
		--build \
		--rm api \
		alembic upgrade head

database_upgrade_dev:
	docker compose \
		-f ./deployments/compose.development.yml \
	 	-p qernel-dev \
		run \
		--build \
		--rm api \
		alembic upgrade head

create_migrations:
	test -n "$(MESSAGE)" || (echo 'Usage: make create_migrations MESSAGE="adds boats table"' && exit 1)
	docker compose \
		-f ./deployments/compose.development.yml \
	 	-p qernel-dev \
		 run \
	 	--rm create_migrations

###
# formatting
###

format:
	${MAKE} format_js
	${MAKE} format_py

format_js:
	@echo ">>> formatting javascript files"
	pnpm format

format_py:
	@echo ">>> formatting python files"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m isort . && \
		python3 -m black .

###
# linting
###

lint:
	${MAKE} lint_py

lint_py:
	@echo ">>> linting python files"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m flake8 .

###
# testing
###

test:
	${MAKE} test_integration
	${MAKE} test_unit

test_integration:
	${MAKE} test_py_integration

test_unit:
	${MAKE} test_py_unit

test_py_integration:
	@echo ">>> running python integration tests"
	source .venv/bin/activate && \
		./scripts/test_py_integration.sh

test_py_unit:
	@echo ">>> running python unit tests"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m pytest -vv -s --log-cli-level=ERROR test/unit

###
# misc.
###

run_api:
	@echo ">>> running api"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m api.main

run_web:
	@echo ">>> running web"
	pnpm start
