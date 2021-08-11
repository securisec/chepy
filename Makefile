.PHONY: test test-report

test:
	pytest --cov-report term-missing --cov=chepy tests

test-report:
	pytest --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/