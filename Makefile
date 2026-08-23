HEADERS := input.h input-event-codes.h uinput.h

src/evdev/ecodes_generated.py:
	uv run python3 src/evdev/genecodes_py.py $(HEADERS:%=/usr/include/linux/%) > $@

docs-live: dev
	uv run sphinx-autobuild --watch src/evdev docs/ docs/_build -E

docs:
	uv run sphinx-build -b html docs docs/_build/html

dev:
	uv pip install -e .

sdist:
	uv build --sdist

bdist:
	git clean -fdx src/
	./scripts/build-binary.sh

.PHONY: docs docs-live sdist bdist dev
