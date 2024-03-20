# pylint: disable=undefined-variable
from setuptools import setup, find_packages
from os import path

# get version and author information
with open("chepy/__version__.py", "r") as f:
    exec(f.read())


def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


requirements = read_requirements()
# if sys.platform == "linux":
#     requirements.append("python-magic")
# else:
#     requirements.append("python-magic-bin==0.4.14")

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), "r", encoding='utf8') as f:
    long_description = f.read()

core_extra_deps = ["requests"]

plugin_deps = [
    "scapy",
    "Markdown",
    "chepy",
    "pefile",
    "pyelftools",
    "ua-parser==0.8.0",
    "pydriller",
    "pyexiftool",
]

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="chepy",
    license="GPL",
    version=__version__,
    author=__author__,
    url="https://github.com/securisec/chepy",
    project_urls={
        "Documentation": "https://chepy.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/securisec/chepy",
    },
    extras_require={"extras": core_extra_deps + plugin_deps},
    packages=find_packages(exclude=(["tests", "docs"])),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    entry_points={"console_scripts": ["chepy = chepy.__main__:main"]},
)
