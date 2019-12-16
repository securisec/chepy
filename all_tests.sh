#!/bin/bash

function check_test {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo -e "\n\033[31;7m$1 Failed" >&2
        exit
    fi
    return $status
}

# pytest and coverage
check_test pytest --disable-pytest-warnings --cov=chepy --cov-config=.coveragerc tests/

# pytest plugins
check_test pytest --disable-pytest-warnings tests_plugins/

# bandit
check_test bandit --recursive chepy/ --ignore-nosec --skip B101,B413,B303,B310,B112,B304,B320,B410,B404

# docs
check_test make -C docs/ clean html

# plugin docs
check_test make -C ~/dev/chepy_plugins/docs clean html

# build docker
# check_test docker build -t chepy .
