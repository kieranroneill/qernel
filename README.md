<div align="center">

[![License: AGPL-3.0](https://img.shields.io/github/license/kieranroneill/qernel)][license]

</div>

<h1 align="center">
  Qernel
</h1>

<p align="center">
  Qernel is a local AI workspace for generating, adapting, and shipping software faster.
</p>

---

### Table of contents

* [1. Overview](#-1-overview)
  - [1.1. Project structure](#11-project-structure)
* [2. Usage](#-2-usage)
  - [2.1. With Docker (Recommended)](#21-with-docker-recommended)
    - [2.1.1. Requirements](#211-requirements)
    - [2.1.2. Set Up Environment](#212-set-up-environment)
    - [2.1.3. Start Docker](#213-start-docker)
  - [2.2. Manual](#22-manual)
    - [2.2.1. Requirements](#221-requirements)
    - [2.2.2. Set Up Environment](#222-set-up-environment)
    - [2.2.3. Start the API](#223-start-the-api)
* [3. Development](#-3-development)
  - [3.1. With Docker (Recommended)](#31-with-docker-recommended)
    - [3.1.1. Requirements](#311-requirements)
    - [3.1.2. Start Docker](#312-start-docker)
* [4. Appendix](#-4-appendix)
  - [4.1. Useful commands](#41-useful-commands)
  - [4.2. Database migrations](#42-database-migrations)
* [5. How to contribute](#-5-how-to-contribute)
* [6. License](#-6-license)

## 🔭 1. Overview

### 1.1. Project structure

```text
.
├─ api/
│   ├── routers/                            <-- FastAPI routers
│   │   └── ...
│   ├── app.py                              <-- FastAPI app initialization
│   ├── main.py                             <-- API entrypoint and server start
│   └── ...
├─ build/
│   ├── package/                            <-- Docker image files
│   │   ├── <service-name>/
│   │   │   ├── Dockerfile
│   │   │   └── Dockerfile.development
│   │   └── ...
│   └── ...
├─ deployments/                             <-- Container orchestration configurations
│   ├── compose.yml
│   └── compose.development.yml
├─ registry/                                <-- Manifests
│   ├── feature-packs/                      <-- Feature pack manifests, e.g. "postgres", "auth-jwt"
│   │   ├── <feature_pack>/
│   │   │   └── pack.yml
│   │   └── ...
│   ├── templates                           <-- App template manifests, e.g. "next-fastapi-saas"
│   │   ├── <template_name>/
│   │   │   ├── files/
│   │   │   │   └── ...
│   │   │   └── template.yml
│   │   └── ...
│   └── ...
├─ test/                                    <-- Test utilities and mocks
│   └── ...
├─ web/
│   ├── main.ts                             <-- Web UI entrypoint
│   └── ...
├── dev-requirements.txt                    <-- Python development dependencies
├── LICENSE                                 <-- Project license
├── Makefile                                <-- Make commands
├── pip-requirements.txt                    <-- Defines the pip version
├── pyproject.toml                          <-- Python project configuration file
├── README.md
├── requirements.txt                        <-- Python dependencies
└── ...
```

<sup>[Back to top ^][table-of-contents]</sup>

## 🪄 2. Usage

### 2.1. With Docker (Recommended)

#### 2.1.1. Requirements

- [Docker](https://docs.docker.com/engine/install/)

<sup>[Back to top ^][table-of-contents]</sup>

#### 2.1.2. Set Up Environment

1. Create a new file `.env.local` at the project root.

2. Add and fill the following values:
* `GITHUB_CLIENT_ID`
* `GITHUB_CLIENT_SECRET`

<sup>[Back to top ^][table-of-contents]</sup>

#### 2.1.3. Start Docker

1. Using Docker compose, you can run the orchestration file using:

```bash
$ make start
```

<sup>[Back to top ^][table-of-contents]</sup>

### 2.2. Manual

#### 2.2.1. Requirements

- [Python v3.11+](https://www.python.org/downloads/)
- [Make](https://www.gnu.org/software/make/)

<sup>[Back to top ^][table-of-contents]</sup>

#### 2.2.2. Set Up Environment

1. Create a new file `.env.local` at the project root.

2. Add and fill the following values:
* `GITHUB_CLIENT_ID`
* `GITHUB_CLIENT_SECRET`

3. Install the dependencies and tools:

```bash
$ make install
```

<sup>[Back to top ^][table-of-contents]</sup>

#### 2.2.3. Start the API

Start the API (this will use a Python virtual environment):

```bash
$ make run_api
```

<sup>[Back to top ^][table-of-contents]</sup>

## 🛠️ 3. Development

### 3.1. With Docker (Recommended)

#### 3.1.1. Requirements

- [Docker](https://docs.docker.com/engine/install/)

<sup>[Back to top ^][table-of-contents]</sup>

#### 3.1.2. Start Docker

1. Using Docker compose, you can run the orchestration file using:

```bash
$ make dev
```

<sup>[Back to top ^][table-of-contents]</sup>

## 📑 4. Appendix

### 4.1. Useful commands

| Command                                                     | Description                                                          |
|-------------------------------------------------------------|----------------------------------------------------------------------|
| `make dev`                                                  | Runs the platform in development mode via Docker.                    |
| `make format`                                               | Formats soruce code files.                                           |
| `make install`                                              | Installs all the dependencies - including development dependencies.  |
| `make install_js_deps`                                      | Installs the JavaScript dependencies.                                |
| `make install_py_deps`                                      | Installs the Python application dependencies.                        |
| `make install_py_dev`                                       | Installs the Python dependencies that inlucde tools for development. |
| `make lint_py`                                              | Lints Python soruce files.                                           |
| `make run_api`                                              | Starts the API in the Python virtual environment.                    |
| `make run_web`                                              | Starts the web application.                                          |
| `make start`                                                | Runs the platform in production mode via Docker.                     |
| `make test`                                                 | Runs all tests.                                                      |
| `make test_py_unit`                                         | Runs Python tests.                                                   |
| `make test_unit`                                            | Runs all unit tests.                                                 |

<sup>[Back to top ^][table-of-contents]</sup>

### 4.2. Database migrations

Database migrations are managed with [Alembic](https://alembic.sqlalchemy.org/en/latest/) and run through Docker, so they use the same environment as the API service.

Use the following commands to create, apply, or roll back migrations:

```shell
make create_migration MESSAGE="adds boats_profiles table"
make database_upgrade
make database_downgrade
```

For development, the matching commands are:

```shell
make database_upgrade_dev
make database_downgrade_dev
```

- `create_migration` generates a new Alembic revision from SQLAlchemy model changes.
- `database_upgrade` applies all pending migrations in the production Compose setup.
- `database_downgrade` rolls back the latest migration in the production Compose setup.
- `database_upgrade_dev` applies all pending migrations in the development Compose setup.
- `database_downgrade_dev` rolls back the latest migration in the development Compose setup.

> ⚠️ **NOTE:** The `MESSAGE` argument is required when creating a migration because it becomes the migration description.

<sup>[Back to top ^][table-of-contents]</sup>

## 👏 5. How to contribute

Please read the [**contributing guide**](https://github.com/kieranroneill/moody-376-assistant/blob/main/CONTRIBUTING.md) to learn about the development process.

<sup>[Back to top ^][table-of-contents]</sup>

## 📄 6. License

Please refer to the [COPYING][license] file.

<sup>[Back to top ^][table-of-contents]</sup>

<!-- links -->

[license]: https://github.com/kieranroneill/qernel/blob/main/COPYING
[table-of-contents]: #table-of-contents
