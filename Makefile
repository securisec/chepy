.PHONY: test test-all


test:
	pytest --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/

test-all: test
	pytest --disable-pytest-warnings tests_plugins/