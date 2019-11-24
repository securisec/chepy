import sys
import inspect
import fire
from docstring_parser import parse as _parse_doc
from chepy import Chepy
from chepy.modules.internal.cli import get_cli_options

chepy = dir(Chepy)


def test_options():
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
            print("Error in method", method)
            raise
    return options


def test_cli_options():
    get_cli_options()


def test_fire1():
    assert fire.Fire(Chepy, command=["A", "-", "to_hex", "o"]) == b"41"


def test_fire2():
    assert (
        fire.Fire(Chepy, command=["abc", "-", "hmac_hash", "--digest", "md5"]).o
        == "dd2701993d29fdd0b032c233cec63403"
    )


def test_fire3():
    fire_obj = fire.Fire(Chepy, command=["abc", "-", "hmac_hash", "--digest", "md5"])
    assert type(fire_obj) == Chepy

