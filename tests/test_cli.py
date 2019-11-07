import sys
import inspect
from docstring_parser import parse as _parse_doc
from chepy import Chepy

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
