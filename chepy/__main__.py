import sys
import inspect
import fire
import regex as re
import argparse
import subprocess
from pathlib import Path
from docstring_parser import parse as _parse_doc
from prompt_toolkit.completion import (
    Completer,
    Completion,
    FuzzyCompleter,
    merge_completers,
)
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

from chepy import Chepy
from chepy.__version__ import __version__
import chepy.modules.internal.cli as chepy_cli
from chepy.modules.internal.colors import red, yellow, cyan, magenta, green
from chepy.config import ChepyConfig

config = ChepyConfig()
options = []
chepy = dir(Chepy)
fire_obj = None
errors = []

prompt_colors = config.prompt_colors.split()


def get_style():
    return Style.from_dict(
        {
            "completion-menu.completion.current": "bg:{}".format(config.prompt_search_background),
            # "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.fuzzymatch.outside": "fg:#00aaaa",
            "prompt1": "{} bold".format(prompt_colors[0]),
            "prompt2": "{} bold".format(prompt_colors[1]),
            "prompt3": "{} bold".format(prompt_colors[2]),
            "state_index": "#ffd700",
            "rprompt": "fg:{}".format(config.prompt_rprompt),
            "bottom-toolbar": config.prompt_bottom_toolbar,
            "prompt_toolbar_version": "bg:{}".format(config.prompt_toolbar_version),
            "prompt_toolbar_states": "bg:{}".format(config.prompt_toolbar_states),
            "prompt_toolbar_buffers": "bg:{}".format(config.prompt_toolbar_buffers),
            "prompt_toolbar_type": "bg:{}".format(config.prompt_toolbar_type),
            "prompt_toolbar_plugins": "bg:{}".format(config.prompt_toolbar_plugins),
            "prompt_toolbar_errors": "bg:{}".format(config.prompt_toolbar_errors),
        }
    )


def get_options():
    global errors
    options = dict()
    for method in chepy:
        try:
            attributes = getattr(Chepy, method)
            if not method.startswith("_") and not isinstance(attributes, property):
                args = inspect.getfullargspec(attributes).args
                parsed_doc = _parse_doc(attributes.__doc__)
                if len(args) == 1:
                    options[method] = {
                        "options": list(
                            map(lambda d: {"flag": d, "meta": ""}, args[1:])
                        ),
                        "meta": parsed_doc.short_description,
                        "returns": parsed_doc.returns.type_name,
                    }
                else:
                    options[method] = {
                        "options": list(
                            map(
                                lambda d: {
                                    "flag": d[1],
                                    "meta": parsed_doc.params[d[0]].description,
                                },
                                enumerate(args[1:]),
                            )
                        ),
                        "meta": parsed_doc.short_description,
                        "returns": parsed_doc.returns.type_name,
                    }
        except:
            e_type, e_msg, e_traceback = sys.exc_info()
            errors.append((e_type.__name__, "Error parsing options in:", method))
            continue
    return options


def prompt_message(fire_obj):
    elements = [
        ("class:prompt1", config.prompt_char),
        ("class:prompt2", config.prompt_char),
        ("class:prompt3", config.prompt_char),
    ]
    try:
        elements.append(
            (
                "class:state_index",
                str(fire_obj._current_index)
                + "/"
                + str(len(fire_obj.current_states) - 1)
                + " ",
            )
        )
    except AttributeError:
        pass
    elements.append(("class:name", " "))
    return elements


def bottom_toolbar(fire_obj):
    global errors
    if isinstance(fire_obj, Chepy):
        states = len(fire_obj.states) - 1 if fire_obj is not None else 0
        current_state = fire_obj._current_index if fire_obj is not None else 0
        buffers = len(fire_obj.buffers) if fire_obj is not None else 0
        return [
            ("class:prompt_toolbar_version", "Chepy: {} ".format(__version__)),
            (
                "class:prompt_toolbar_states",
                " States: {current}/{total} ".format(
                    current=current_state, total=states
                ),
            ),
            (
                "class:prompt_toolbar_buffers",
                " Buffers: {total} ".format(total=buffers),
            ),
            (
                "class:prompt_toolbar_type",
                " State: {} ".format(type(fire_obj.state).__name__),
            ),
            (
                "class:prompt_toolbar_plugins",
                " Plugins: {} ".format(config.enable_plugins),
            ),
            ("class:prompt_toolbar_errors", " Errors: {} ".format(len(errors))),
        ]


class CustomValidator(Validator):
    def validate(self, document):
        text = document.text.split()
        if re.search(r"^(!|#|\?)", document.text):
            pass
        elif len(text) > 1:
            if not text[-2].startswith("--"):
                if (
                    not re.search(r"\"|'", text[-1])
                    and not text[-1].startswith("--")
                    and text[-1] not in list(get_options().keys())
                ):
                    raise ValidationError(
                        cursor_position=1,
                        message="{text} is not a valid Chepy method".format(
                            text=text[-1]
                        ),
                    )


class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        global options
        method_dict = get_options()
        word = document.get_word_before_cursor()

        methods = list(method_dict.items())

        selected = document.text.split()
        if len(selected) > 0:
            selected = selected[-1]
            if selected.startswith("cli_"):
                methods = options
            elif not selected.startswith("--"):
                current = method_dict.get(selected)
                if current is not None:
                    has_options = method_dict.get(selected)["options"]
                    if has_options is not None:
                        options = [
                            ("--{}".format(o["flag"]), {"meta": o["meta"]})
                            for o in has_options
                        ]
                        methods = options + methods
            else:
                methods = options

        for method_name, method_docs in methods:
            if method_name.startswith(word):
                meta = (
                    method_docs["meta"]
                    if isinstance(method_docs, dict) and method_docs.get("meta")
                    else ""
                )
                not_chepy_obj = ""
                if method_docs.get("returns"):
                    if method_docs["returns"] is None:
                        not_chepy_obj = "bg:{}".format(config.prompt_cli_method)
                    elif method_docs["returns"] == "ChepyPlugin":
                        not_chepy_obj = "bg:{}".format(config.prompt_plugin_method)
                yield Completion(
                    method_name,
                    start_position=-len(word),
                    display_meta=meta,
                    style=not_chepy_obj,
                )


def get_current_type(obj):
    if config.show_rprompt:
        if obj:
            return type(obj).__name__
        else:
            return "Type of current state"
    else:
        return None


def parse_args(args):
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parse.add_argument(
        "-r", "--recipe", dest="recipe", help="Run a Chepy recipe and exit"
    )
    parse.add_argument("data", nargs="+")
    return parse.parse_args(args)


def main():
    global fire_obj
    last_command = []

    args = parse_args(sys.argv[1:])
    args_data = args.data

    if args.recipe:
        print(Chepy(*args_data).load_recipe(args.recipe).o)
    else:
        args_data.append("-")

        history_file = config.history_path
        session = PromptSession(
            history=FileHistory(history_file),
            style=get_style(),
            wrap_lines=True,
            auto_suggest=AutoSuggestFromHistory(),
        )
        try:
            while True:
                prompt = session.prompt(
                    prompt_message(fire_obj=fire_obj),
                    bottom_toolbar=bottom_toolbar(fire_obj),
                    completer=FuzzyCompleter(
                        merge_completers([CustomCompleter(), chepy_cli.CliCompleter()])
                    ),
                    validator=CustomValidator(),
                    rprompt=get_current_type(fire_obj),
                )

                # check and output any commands that start with cli_
                if re.match(r"^\!", prompt):
                    print(magenta(subprocess.getoutput(re.sub(r"^\!\s?", "", prompt))))
                # check if line is a comment
                elif re.match(r"^#", prompt):
                    print(cyan(prompt))
                # get help for a method
                elif re.match(r"^\?", prompt):
                    _method_name = re.match(r"^\?(\s?)+([\w_]+)", prompt).group(2)
                    chepy_cli.get_doc(_method_name)
                # check if method called is a cli method
                elif re.search(r"^cli_.+", prompt):
                    cli_method = prompt.split()[0]
                    cli_args = re.search(r"--(\w+)\s([\w\W]+)", prompt)
                    # Show errors encountered
                    if cli_method == "cli_show_errors":
                        getattr(chepy_cli, "cli_show_errors")(errors)
                    # show the current plugin path
                    elif cli_method == "cli_plugin_path":
                        getattr(chepy_cli, "cli_plugin_path")(config)
                    # Edit the current state
                    elif cli_method == "cli_edit_state":
                        try:
                            getattr(chepy_cli, "cli_edit_state")(fire_obj, args_data)
                            args_data = args_data[0 : args_data.index("-")] + ["-"]
                        except:
                            e_type, e_msg, e_traceback = sys.exc_info()
                            print(red(e_type.__name__), yellow("Could not edit state"))
                    # Go back one step
                    elif cli_method == "cli_go_back":
                        args_data = args_data[: -len(last_command + ["-"])]
                        print(cyan("Go back: {}".format(last_command)))
                    # Delete the cli history file
                    elif cli_method == "cli_delete_history":
                        Path(config.history_path).unlink()
                    elif cli_args:
                        getattr(chepy_cli, cli_method)(
                            fire_obj, **{cli_args.group(1): cli_args.group(2)}
                        )
                    else:
                        getattr(chepy_cli, cli_method)(fire_obj)

                else:
                    for method in chepy:
                        if not method.startswith("_") and not isinstance(
                            getattr(Chepy, method), property
                        ):
                            fire.decorators._SetMetadata(
                                getattr(Chepy, method),
                                fire.decorators.ACCEPTS_POSITIONAL_ARGS,
                                False,
                            )
                    args_data += prompt.split()
                    if args_data[-1] != "-":
                        args_data.append("-")
                    try:
                        last_command = prompt.split() + ["-"]
                        fire_obj = fire.Fire(Chepy, command=args_data)
                    # handle required args for methods
                    except fire.core.FireExit:
                        args_data = args_data[: -len(last_command)]
                    except TypeError as e:
                        print(red(e.message))
                    except SystemExit:
                        sys.exit()
                    except:
                        # go back to last working arg
                        e_type, e_msg, e_traceback = sys.exc_info()
                        print(red(e_type.__name__), yellow(e_msg.__str__()))
                        args_data = args_data[: -len(last_command)]
                        continue
        except KeyboardInterrupt:
            print(green("\nOKBye"))
            sys.exit()
        except EOFError:
            print(green("\nOKBye"))
            sys.exit()

