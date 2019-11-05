import inspect
import fire
import regex as re
from pathlib import Path
import argparse
from tempfile import gettempdir
from docstring_parser import parse as _parse_doc
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from chepy import Chepy
from chepy.__version__ import __version__


options = []
chepy = dir(Chepy)


def get_style():
    return Style.from_dict(
        {
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            # "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion fuzzymatch.outside": "fg:#000000",
            "name": "#ffd700",
            "file": "#00ff48",
        }
    )


def get_options():
    options = dict()
    for method in chepy:
        try:
            attributes = getattr(Chepy, method)
            if not method.startswith("_") and not isinstance(attributes, property):
                args = inspect.getfullargspec(attributes).args
                parsed_doc = _parse_doc(attributes.__doc__)
                if len(args) == 1:
                    options[method] = {
                        "options": list(map(lambda d: {"flag": d, "meta": ""}, args[1:])),
                        "meta": parsed_doc.short_description,
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
                    }
        except:
            continue
    return options


def prompt_message(args: argparse.ArgumentParser):
    elements = [("class:name", "[Chepy {}] # ".format(__version__))]
    if args.file:
        elements.append(("class:file", "File "))
    return elements


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
            if not selected.startswith("--"):
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

        for m in methods:
            if m[0].startswith(word):
                meta = (
                    m[1]["meta"] if isinstance(m[1], dict) and m[1].get("meta") else ""
                )
                yield Completion(m[0], start_position=-len(word), display_meta=meta)


def main():
    parse = argparse.ArgumentParser()
    types = parse.add_mutually_exclusive_group()
    types.add_argument("--file", action="store_true", dest="file", default=False)
    parse.add_argument("data", nargs=1)
    args = parse.parse_args()

    base_command = '--data "{data}" --is_file={file} '.format(
        data="".join(args.data), file=args.file
    )

    history_file = str(Path(gettempdir() + "/chepy"))
    session = PromptSession(
        history=FileHistory(history_file), style=get_style(), wrap_lines=True
    )
    try:
        while True:
            prompt = session.prompt(
                prompt_message(args),
                completer=FuzzyCompleter(CustomCompleter()),
                validator=CustomValidator(),
            )
            # command = re.findall(r'(?:".*?"|\S)+', prompt)
            base_command += " " + prompt
            for method in chepy:
                if not method.startswith("_") and not isinstance(
                    getattr(Chepy, method), property
                ):
                    fire.decorators._SetMetadata(
                        getattr(Chepy, method),
                        fire.decorators.ACCEPTS_POSITIONAL_ARGS,
                        False,
                    )
            fire.Fire(Chepy, command=base_command)
    except KeyboardInterrupt:
        print("OKBye")
        exit()
