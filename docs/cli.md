# Chepy CLI

Chepy CLI is a fully dynamically generated cli that combines the power for python-fire and prompt_toolkit to create its cli. The cli is used very similar to how the main `Chepy` class is used as it allows for method chaining. We know from the docs that some of the methods in the `Chepy` class takes optional or required arguments. In the cli, these are passed as flags. Refer to the [examples](./examples.md) for use cases.

## Cli options
```bash
usage: chepy [-h] [-v] [-r RECIPE] [data [data ...]]

positional arguments:
  data

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -r RECIPE, --recipe RECIPE
```

## Cli magic markers
There are three special characters in the cli.

- `!` If a line begins with `!` it is interpreted as a shell command. For example: `! ls -la`
- `#` If a line begins with `#` it is interpreted as a comment. For example: `# hello`
- `?` If a line begins with `?` it provides help for the provided Chepy method. For example: `? to_hex`

### Cli Recipes
The cli can be run in a non interactive mode using the `-r` flag. This flag will load the recipe that is supplied and run it on the arguments that is provided.

```bash
# Example
chepy -r test.recipe a.png
```

### Using builtins

One of the more advanced functions of the cli allows the user to use arbitrary builtin methods when the state does not contain a Chepy object. 

Consider this example in code. We will parse a User agent string in this case:
```python
>>> ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
>>> c = Chepy(ua).parse_user_agent()
{'user_agent': {'family': 'Other', 'major': None, 'minor': None, 'patch': None}, 'os': {'family': 'Other', 'major': None, 'minor': None, 'patch': None, 'patch_minor': None}, 'device': {'family': 'Other', 'brand': None, 'model': None}, 'string': 'ua'}
# The state type currently is Chepy
>>> c.o
# The state type now is a dict
>>> c.get("user_agent").get("family")
"Chrome"
# we are using the dict builtin method get to pull the values based on keys
```

This same behavior is replicated in the Chepy cli.

[![asciicast](https://asciinema.org/a/BTBg3PLFeiN21UBcpjYxWWLnc.svg)](https://asciinema.org/a/BTBg3PLFeiN21UBcpjYxWWLnc)

### Cli only methods
For completeness sake everything is document here, but the only functions that are callable from the CLI are functions that start with `cli_`. 

### Cli shell commands
It is possible to run shell commands from the cli py starting the command with a `!`. 

```bash
>>> !ls -la | grep py
```
This will run the following command inside the Chepy cli

```eval_rst
.. automodule:: chepy.modules.internal.cli
    :members:
```