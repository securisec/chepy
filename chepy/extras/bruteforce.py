import zipfile
from pathlib import Path


def _expand_path(path):
    return str(Path(path).expanduser().absolute())


def zip_password_bruteforce(path: str, wordlist: str) -> str:
    z = zipfile.ZipFile(_expand_path(path))
    with open(_expand_path(wordlist)) as f:
        for password in f:
            password = password.strip().encode()
            try:
                z.setpassword(password)
                z.testzip()
                return password
            except RuntimeError:  # pragma: no cover
                continue
