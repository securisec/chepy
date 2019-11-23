# Pull requests

Pull requests for Chepy are very welcome, but the following guidelines needs to be followed. 

## Code Style
Chepy uses [python black](https://github.com/psf/black) for its code style and formatting. All pull requests should have proper formatting applied.

## Commit messages
Commit messages should always have proper flair indicating the changes. The first line of the commit message should include the emojis of what was changed followed by multiline description of what was added. 

### Example commit message
```
✅🔅ℹ️🧨📚

🔅 added new ability
🧨 refactored something
ℹ️ updated something
ℹ️ fixed something
✅ added a new method
✅ added another new method
📚 added new docs
```

### The current flairs in use are:

- 🔅 A new feature has been added. This could be tests files, new arguments etc.
- ℹ️ An update has been made to an existing feature
- 🧨 A major refactor has taken place. This could be anything in the Cli or ChepyCore classes.
- 🐍 A new python dependency has been added
- ✅ New method has been added
- 📚 Added new documentation

## Tests
Chepy maintains a 100% Codecov coverage, and all pull requests are required to submit complimentary tests. The tests should include all paths, including coverage for optional arguments, if loops etc. Failing the 100% coverage will automatically fail the configured Github Actions.

Tests requires the following dev dependencies:
- pytest
- pytest-cov
- sphinx
- recommonmark
- bandit

To run tests for coverage and pytest, use:
```bash
pytest --disable-pytest-warnings --cov-report=xml --cov=chepy --cov-config=.coveragerc tests/
```

For bandit tests, use:
```bash
bandit --recursive chepy/ --ignore-nosec --skip B101,B413,B303,B310,B112,B304,B320,B410
```

Finally for docs tests, use:
```bash
make -C docs/ clean html
```

The most convenient way to run all the tests are via the handy `all_tests.sh` from the root directory. 
