# pylint: disable=undefined-variable
from setuptools import setup, find_packages
from os import path
from shutil import copy
from pathlib import Path
from configparser import ConfigParser

# create .chefy dir in home and move base conf file if it does not exist
home = Path.home()
chepy_dir = Path(home / ".chepy")
chepy_conf = Path(chepy_dir / "chepy.conf")
rc_path = Path("chepy.conf").absolute()

Path(chepy_dir).mkdir(exist_ok=True)
# Chepy default configs
config = ConfigParser()
config.read(str(rc_path))
# history file
config["Cli"]["HistoryPath"] = str(chepy_dir / "chepy_history")
Path(str(chepy_dir / "chepy_history")).touch(exist_ok=True)
# if file already exists, do not overwrite it
if not chepy_conf.exists():
    with open(str(chepy_conf), "w") as f:
        config.write(f)

# get version and author information
with open("chepy/__version__.py", "r") as f:
    exec(f.read())


def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="chepy",
    version=__version__,
    author=__author__,
    packages=find_packages(exclude=(["tests", "docs"])),
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["chepy = chepy.__main__:main"]},
)
