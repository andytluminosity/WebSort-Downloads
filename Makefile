.PHONY: py-lint

py-lint:
	cd python_server && \
	mypy . && \
	ruff format && \
	ruff check --fix