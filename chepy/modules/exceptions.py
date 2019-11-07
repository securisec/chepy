import sys
from functools import wraps

from chepy.modules.internal.colors import Color_RED


def exception_handler(func):
    @wraps(func)
    def l(*args, **kwargs):
        try:
            o = func(*args, **kwargs)
            return o
        except Exception as e:
            if sys.stdout.isatty():
                e_type, e_msg, e_traceback = sys.exc_info()
                return Color_RED(e_type.__name__) + " " + str(e_msg)
            else:
                raise

    return l


class PrintException(Exception):
    pass
