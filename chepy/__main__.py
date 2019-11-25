import sys
import inspect
import fire
import regex as re
from pathlib import Path
import argparse
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
from chepy.modules.internal.colors import RED, YELLOW
from .conf import Config

config = Config()
options = []
chepy = dir(Chepy)
fire_obj = None
errors = []


def get_style():
    return Style.from_dict(
        {
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            # "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.fuzzymatch.outside": "fg:#00aaaa",
            "name1": "#00ffff bold",
            "name2": "#ff0000 bold",
            "name3": "#ffd700 bold",
            "state_index": "#ffd700",
            "file": "#00ff48",
            "rprompt": "fg:#00ff48",
            "bottom-toolbar": "#000000",
            "bt_version": "bg:#00ff48",
            "bt_states": "bg:#60cdd5",
            "bt_buffers": "bg:#ff00ff",
            "bt_type": "bg:#ffd700",
            "bt_errors": "bg:#ff0000",
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
    elements = [("class:name1", ">"), ("class:name2", ">"), ("class:name3", ">")]
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
            ("class:bt_version", "Chepy: {} ".format(__version__)),
            (
                "class:bt_states",
                " States: {current}/{total} ".format(
                    current=current_state, total=states
                ),
            ),
            ("class:bt_buffers", " Buffers: {total} ".format(total=buffers)),
            ("class:bt_type", " State: {} ".format(type(fire_obj.state).__name__)),
            ("class:bt_errors", " Errors: {} ".format(len(errors))),
        ]


class CustomValidator(Validator):
    def validate(self, document):
        text = document.text.split()
        if len(text) > 1:
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
                    if method_docs["returns"] != "Chepy":
                        not_chepy_obj = "bg:#ffd700"
                yield Completion(
                    method_name,
                    start_position=-len(word),
                    display_meta=meta,
                    style=not_chepy_obj,
                )


def get_current_type(obj):
    if obj:
        return type(obj).__name__
    else:
        return "Type of current state"


def parse_args(args):
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parse.add_argument("data", nargs="*")
    return parse.parse_args(args)


def main():
    global fire_obj
    last_command = []

    args = parse_args(sys.argv[1:])
    args_data = args.data

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
            if re.search(r"^cli_.+", prompt):
                cli_method = prompt.split()[0]
                cli_args = re.search(r"--(\w+)\s(\w+)", prompt)
                if cli_method == "cli_show_errors":
                    getattr(chepy_cli, "cli_show_errors")(errors)
                elif cli_method == "cli_go_back":
                    args_data = args_data[: -len(last_command + ["-"])]
                elif cli_method == 'cli_delete_history':
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
                except:
                    # go back to last working arg
                    e_type, e_msg, e_traceback = sys.exc_info()
                    print(RED(e_type.__name__), YELLOW(e_msg.__str__()))
                    args_data = args_data[: -len(last_command)]
                    continue
    except KeyboardInterrupt:
        print("OKBye")
        exit()
