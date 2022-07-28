.PHONY: test test-all


test:
	pytest -v --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/

test-all: test
	pytest -v --disable-pytest-warnings tests_plugins/