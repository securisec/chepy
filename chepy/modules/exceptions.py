import sys
from decorator import decorator

from chepy.modules.internal.colors import RED


@decorator
def exception_handler(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if sys.stdout.isatty():
            e_type, e_msg, e_traceback = sys.exc_info()
            return RED(e_type.__name__) + " " + str(e_msg)
        else:
            raise


class PrintException(Exception):
    pass
