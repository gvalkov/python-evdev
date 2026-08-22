docs-live:
	uv run sphinx-autobuild docs/ docs/_build

docs:
	uv run sphinx-build -b html docs docs/_build/html

dev:
	uv pip install -e .

sdist:
	uv build

bdist:
	git clean -fdx src/
	./scripts/build-binary.sh

.PHONY: docs docs-live sdist bdist dev
