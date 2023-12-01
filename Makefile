sources = src tests

.PHONY: lint
lint:
	pdm run ruff $(sources)

.PHONY: fix
fix:
	pdm run ruff --fix $(sources)

.PHONY: format
format:
	pdm run ruff format $(sources)

.PHONY: mypy
mypy:
	pdm run mypy $(sources)

.PHONY: codespell
codespell:
	pre-commit run codespell --all-files

.PHONY: tests
tests:
	pdm run pytest -vv -s

.PHONY: cov
cov:
	pdm run pytest --cov=src --cov-fail-under=80
