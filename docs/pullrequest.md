# Pull requests

Pull requests for Chepy are very welcome, but the following guidelines needs to be followed. 

## Code Style
Chepy uses [python black](https://github.com/psf/black) for its code style and formatting. All pull requests should have proper formatting applied.

## Commit messages
Commit messages should always have proper flair indicating the changes. The current flairs in use are:

- 🔅 A new feature has been added. This could be tests files, new arguments etc.
- ℹ️ An update has been made to an existing feature
- 🧨 A new python dependency has been added
- 🔍 A major refactor has taken place. This could be anything in the Cli or Core classes.
- ✅ New method has been added

## Tests
Chepy maintains a 100% Codecov coverage, and all pull requests are required to submit complimentary tests. The tests should include all paths, including coverage for optional arguments, if loops etc. Failing the 100% coverage will automatically fail the configured Github Actions.
