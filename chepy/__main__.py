import fire
from chepy import Chepy


def main():
    for method in dir(Chepy):
        if not method.startswith("_") and not isinstance(
            getattr(Chepy, method), property
        ):
            fire.decorators._SetMetadata(
                getattr(Chepy, method), fire.decorators.ACCEPTS_POSITIONAL_ARGS, False
            )
    fire.Fire(Chepy)
    # todo use command=[list of str] to run the command from prompt-toolkit
    # todo save the value of --data to a state to reset state back to original
    # todo option to save final output to state
    # todo theming of prompt
