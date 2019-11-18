import sys
from colorama import Fore, init

# init(convert=True)


def RED(s: str) -> str:  # pragma: no cover
    """Red color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import RED
        >>> print(RED("some string"))
    """
    if sys.stdout.isatty():
        return Fore.RED + s + Fore.RESET
    else:
        return s


def LIGHT_RED(s: str) -> str:  # pragma: no cover
    """Light red color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string
    
    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_RED
        >>> print(LIGHT_RED("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTRED_EX + s + Fore.RESET
    else:
        return s


def BLUE(s: str) -> str:  # pragma: no cover
    """Blue color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import BLUE
        >>> print(BLUE("some string"))
    """
    # if sys.stdout.isatty():
    return Fore.BLUE + s + Fore.RESET
    # else:
    #     return s


def LIGHT_BLUE(s: str) -> str:  # pragma: no cover
    """Light blue color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_BLUE
        >>> print(LIGHT_BLUE("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTBLUE_EX + s + Fore.RESET
    else:
        return s


def CYAN(s: str) -> str:  # pragma: no cover
    """Cyan color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import CYAN
        >>> print(CYAN("some string"))
    """
    if sys.stdout.isatty():
        return Fore.CYAN + s + Fore.RESET
    else:
        return s


def LIGHT_CYAN(s: str) -> str:  # pragma: no cover
    """Light cyan color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_CYAN
        >>> print(LIGHT_CYAN("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTCYAN_EX + s + Fore.RESET
    else:
        return s


def GREEN(s: str) -> str:  # pragma: no cover
    """Green color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import GREEN
        >>> print(GREEN("some string"))
    """
    if sys.stdout.isatty():
        return Fore.GREEN + s + Fore.RESET
    else:
        return s


def LIGHT_GREEN(s: str) -> str:  # pragma: no cover
    """Light green color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_GREEN
        >>> print(LIGHT_GREEN("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    else:
        return s


def YELLOW(s: str) -> str:  # pragma: no cover
    """Yellow color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import YELLOW
        >>> print(YELLOW("some string"))
    """
    if sys.stdout.isatty():
        return Fore.YELLOW + s + Fore.RESET
    else:
        return s


def LIGHT_YELLOW(s: str) -> str:  # pragma: no cover
    """Light yellow color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_YELLOW
        >>> print(LIGHT_YELLOW("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    else:
        return s


def MAGENTA(s: str) -> str:  # pragma: no cover
    """Magenta color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import MAGENTA
        >>> print(MAGENTA("some string"))
    """
    if sys.stdout.isatty():
        return Fore.MAGENTA + s + Fore.RESET
    else:
        return s


def LIGHT_MAGENTA(s: str) -> str:  # pragma: no cover
    """Light magenta color string if tty
    
    Args:
        s (str): String to color
    
    Returns:
        str: Colored string

    Examples:
        >>> from chepy.modules.internal.colors import LIGHT_MAGENTA
        >>> print(LIGHT_MAGENTA("some string"))
    """
    if sys.stdout.isatty():
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET
    else:
        return s

