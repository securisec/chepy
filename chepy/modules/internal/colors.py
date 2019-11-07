import sys
from colorama import Fore


def Color_RED(s):
    if sys.stdout.isatty():
        return Fore.RED + s + Fore.RESET
    else:
        return s


def Color_LIGHT_RED(s):
    if sys.stdout.isatty():
        return Fore.LIGHTRED_EX + s + Fore.RESET
    else:
        return s


def Color_BLUE(s):
    if sys.stdout.isatty():
        return Fore.BLUE + s + Fore.RESET
    else:
        return s


def Color_LIGHT_BLUE(s):
    if sys.stdout.isatty():
        return Fore.LIGHTBLUE_EX + s + Fore.RESET
    else:
        return s


def Color_CYAN(s):
    if sys.stdout.isatty():
        return Fore.CYAN + s + Fore.RESET
    else:
        return s


def Color_LIGHT_CYAN(s):
    if sys.stdout.isatty():
        return Fore.LIGHTCYAN_EX + s + Fore.RESET
    else:
        return s


def Color_GREEN(s):
    if sys.stdout.isatty():
        return Fore.GREEN + s + Fore.RESET
    else:
        return s


def Color_LIGHT_GREEN(s):
    if sys.stdout.isatty():
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    else:
        return s


def Color_YELLOW(s):
    if sys.stdout.isatty():
        return Fore.YELLOW + s + Fore.RESET
    else:
        return s


def Color_LIGHT_YELLOW(s):
    if sys.stdout.isatty():
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    else:
        return s


def Color_MAGENTA(s):
    if sys.stdout.isatty():
        return Fore.MAGENTA + s + Fore.RESET
    else:
        return s


def Color_LIGHT_MAGENTA(s):
    if sys.stdout.isatty():
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET
    else:
        return s

