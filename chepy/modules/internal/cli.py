import sys
import inspect
import regex as re
import pprint

from docstring_parser import parse as _parse_doc
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

from chepy import Chepy
from chepy.config import ChepyConfig
from chepy.modules.internal.colors import yellow, red, yellow_background

pprint.sorted = lambda x, key=None: x

module = sys.modules[__name__]
options = []
config = ChepyConfig()


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


def get_doc(method: str):
    """Get docs for a method"""
    try:
        print(yellow(getattr(Chepy, method).__doc__))
    except:
        print(red(pprint.pformat("Could not find docs...")))


# def cli_edit_state(fire: object, args: list):
#     """Edit the current state

#     Args:
#         args (object): Cli args
#     """
#     current_index = fire._current_index
#     hold = editor.edit(contents=str(fire.states[current_index])).decode()
#     args[current_index] = hold


def cli_highlight(fire: object, highlight: str):
    """Highlight regex match for cli
    
    Args:
        fire (object): The fire object.
        highlight (str): Regex to highlight
    """
    current_state = fire.states[fire._current_index]
    if fire is not None and isinstance(fire, Chepy):
        try:
            print(
                re.sub(
                    "({})".format(highlight),
                    yellow_background(r"\1"),
                    str(current_state),
                )
            )
        except:
            red("Could not highlight because state is not a string")
        # elif type(current_state) == bytes or type(current_state) == bytearray:
        #     print(re.sub('({})'.format(highlight).encode(), red(r'\1').encode(), current_state).decode())
    else:
        print(type(fire))


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


def print_in_colors(out):
    style = Style.from_dict({"cli_out": "fg:{}".format(config.cli_info_color)})
    print_formatted_text(FormattedText([("class:cli_out", str(out))]), style=style)


def cli_state_type(fire: object):
    """Get the current state type
    
    Args:
        fire (object): The fire object
    """
    if fire is not None and isinstance(fire, Chepy):
        print_in_colors(type(fire.state))
    else:
        print(type(fire))


def cli_get_state(fire: object, index: int):
    """Change the current state
    
    Args:
        fire (object): The fire object
        index (int): Required. The index for the state
    """
    if fire is not None and isinstance(fire, Chepy):
        print_in_colors(fire.states[int(index)])
    else:
        print(type(fire))


def cli_show_length(fire: object):
    """Get the length of the current state.

    Args:
        fire (object): The fire object
    """
    print_in_colors(len(fire.state))


def cli_show_dict_keys(fire: object, pretty: bool = False):
    """Get the dict keys of the current state.

    Args:
        fire (object): The fire object
        pretty (bool): Pretty print output. Defaults to False
    """
    if pretty:
        print_in_colors(pprint.pformat(list(fire.state.keys())))
    else:
        print_in_colors(fire.state.keys())


def cli_show_states(fire: object, pretty: bool = False):
    """Change the current state
    
    Args:
        fire (object): The fire object
        pretty (bool): Pretty print output. Defaults to False
    """
    if fire is not None and isinstance(fire, Chepy):
        if pretty:
            print_in_colors(pprint.pformat(fire.states))
        else:
            print_in_colors(fire.states)
    else:
        print(type(fire))


def cli_show_buffers(fire: object, pretty: bool = False):
    """Show all current buffers
    
    Args:
        fire (object): The fire object
        pretty (bool): Pretty print output. Defaults to False
    """
    if fire is not None and isinstance(fire, Chepy):
        if pretty:
            print_in_colors(pprint.pformat(fire.buffers))
        else:
            print_in_colors(fire.buffers)
    else:
        print(type(fire))


def cli_get_attr(fire: object, attr: str):
    """Get attributes from current state type
    
    Args:
        fire (object): The fire object
        attr (str): Required. A valid attr name
    """
    if fire is not None and not isinstance(fire, Chepy):
        print_in_colors(getattr(fire, attr)())
    else:
        print(red("Nope. That didn't work.."))


def cli_pretty_print(fire: object):
    """Pretty print the current state
    
    Args:
        fire (object): The fire object
    """
    if fire is not None and isinstance(fire, Chepy):
        print_in_colors(pprint.pformat(fire.state))
    else:
        print(red("Nope. That didn't work.."))


def cli_plugin_path(config):
    """Print the current plugin path
    """
    print(yellow(str(config.plugin_path)))


def cli_show_errors(errors):
    """Show the errors messages if any
    """
    pprint.pprint(errors)


def cli_go_back():
    """Go back one step
    """
    pass


def cli_delete_history():
    """Delete local history file
    """
    pass


def cli_exit(fire: object):
    """Exit the cli
    
    Args:
        fire (object): The fire object
    """
    exit()
