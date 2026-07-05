SHELL := /bin/bash

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
	 	--env-file .env.dev \
		up \
		--build

start:
	docker compose \
		-f ./deployments/compose.yml \
		--env-file .env \
		up \
		--build

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
	${MAKE} test_unit

test_unit:
	${MAKE} test_py_unit

test_py_unit:
	@echo ">>> running python unit tests"
	python3 -m venv .venv
	source .venv/bin/activate && \
		python3 -m pytest -vv -s --log-cli-level=ERROR api

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
