.PHONY: test test-all


test:
	COVERAGE_CORE=sysmon python -m pytest --noconftest -v --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/

test-all: test
	COVERAGE_CORE=sysmon python -m pytest --noconftest -v --disable-pytest-warnings tests_plugins/

# git log --format=%B 4.0.0..5.0.0 | sed '/^\s*$/d' | sort | uniq