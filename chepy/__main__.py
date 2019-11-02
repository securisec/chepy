import fire
from chepy import Chepy


def main():
    for method in dir(Chepy):
        if not method.startswith("_"):
            fire.decorators._SetMetadata(
                getattr(Chepy, method), fire.decorators.ACCEPTS_POSITIONAL_ARGS, False
            )
    fire.Fire(Chepy)
