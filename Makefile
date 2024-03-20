.PHONY: test test-all


test:
	python -m pytest -v --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/

test-all: test
	python -m pytest -v --disable-pytest-warnings tests_plugins/

# git log --format=%B 4.0.0..5.0.0 | sed '/^\s*$/d' | sort | uniq