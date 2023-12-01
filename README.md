# One time sectet 1440 — share a secret

[![Build and push image](https://github.com/0x12th/onetimesecret-1440/actions/workflows/image.yml/badge.svg)](https://github.com/0x12th/onetimesecret-1440/actions/workflows/image.yml) [![Lints](https://github.com/0x12th/onetimesecret-1440/actions/workflows/lints.yml/badge.svg)](https://github.com/0x12th/onetimesecret-1440/actions/workflows/lints.yml) [![Tests](https://github.com/0x12th/onetimesecret-1440/actions/workflows/tests.yml/badge.svg)](https://github.com/0x12th/onetimesecret-1440/actions/workflows/tests.yml) [![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/0x12th/539a3c90f92bfc4707c73ea2fd910b65/raw/covbadge.json)](https://github.com/0x12th/onetimesecret-1440/actions/workflows/tests.yml)

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org) [![code style - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-202235.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)

#### [Docker Hub image link](https://hub.docker.com/repository/docker/0x12th/ots/)

## For run prod version
```bash
  docker compose -f ./docker-compose/docker-compose.prod.yml up -d
```


## API Reference

#### Generate a secret code that can be used to get the secret

```http
  POST /generate
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `secret_message` | `string` | **Required**. Sectet message |
| `passphrase` | `string` | **Required**. Passphrase |
| `ttl` | `int` | **Optional**. Secret lifetime in seconds |

#### Response: secret_key (str)

#### Get secret

```http
  POST /secrets/{secret_key}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `secret_key`      | `string` | **Required**. Generated secret code that used to get the secret |
| `passphrase` | `string` | **Required**. Passphrase |

#### Response: secret_message (str)


## Environment Variables
Depending on the app run, copy the values from *-example.env to .env

#### prod-example.env
for run prod version

#### dev-example.env
for local dev with db in container


## Local development
```bash
  docker compose -f ./docker-compose/docker-compose.db.yml up -d --build
  pdm install
  pdm start
```

### Migrations
- create migration
```bash
pdm run alembic revision -m *migration_name* --autogenerate
```
- run migrations
```bash
pdm run alembic upgrade head
```
- downgrade migration
```bash
pdm run alembic downgrade -1  # or -2 or base or hash of the migration
```
### Tests
> in pytest.ini
>
> - for github action set:
> POSTGRES_DSN=postgresql+asyncpg://ots:ots@ots_db/postgres
>
> - for local dev db in container only set:
> POSTGRES_DSN=postgresql+asyncpg://onetimesecret:onetimesecret@localhost:65432/onetimesecret

- run tests
```bash
pdm run pytest
```
- run test coverage
```bash
pdm run pytest --cov=src --cov-fail-under=80
```
