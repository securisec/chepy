import sys
import inspect
from docstring_parser import parse as _parse_doc
from prompt_toolkit.completion import Completer, Completion

from chepy import Chepy

module = sys.modules[__name__]
options = []


class CliCompleter(Completer):
    def get_completions(self, document, complete_event):
        global options
        method_dict = get_cli_options()
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

        for method_name, method_docs in methods:
            if method_name.startswith(word):
                meta = (
                    method_docs["meta"]
                    if isinstance(method_docs, dict) and method_docs.get("meta")
                    else ""
                )
                not_chepy_obj = ""
                if method_name.startswith("cli_"):
                    not_chepy_obj = "bg:#00ff00 #0000ff"
                yield Completion(
                    method_name,
                    start_position=-len(word),
                    display_meta=meta,
                    style=not_chepy_obj,
                )


def functions_cli():
    """Get all the function names from this module"""
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__name__.startswith("cli_"):
            functions.append(obj.__name__)
    return functions


def get_cli_options():
    options = dict()
    for method in functions_cli():
        try:
            attributes = getattr(module, method)
            if not method.startswith("_"):
                args = inspect.getfullargspec(attributes).args
                parsed_doc = _parse_doc(attributes.__doc__)
                if len(args) == 1:
                    options[method] = {
                        "options": list(
                            map(lambda d: {"flag": d, "meta": ""}, args[1:])
                        ),
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
            raise
    return options


def cli_state_type(fire: object):
    """Get the current state type
    
    Args:
        fire (object): The fire object
    """
    if fire is not None and isinstance(fire, Chepy):
        print(type(fire.state))
    else:
        print(type(fire))


def cli_type_attr(fire: object, attr: str):
    """Get attributes from current state type
    
    Args:
        fire (object): The fire object
        attr (str): A valid attr name
    """
    if fire is not None and not isinstance(fire, Chepy):
        print(getattr(fire, attr)())
    else:
        print('nope')


def cli_exit(fire: object):
    """Exit the cli
    
    Args:
        fire (object): The fire object
    """
    exit()
