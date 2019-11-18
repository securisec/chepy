#!/bin/bash

# pytest and coverage
pytest --disable-pytest-warnings --cov=chepy --cov-config=.coveragerc tests/

# bandit
bandit --recursive chepy/ --ignore-nosec --skip B101,B413,B303,B310,B112,B304,B320,B410

# docs
make -C docs/ clean html
