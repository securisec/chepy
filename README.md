<p align="center">
    <img src="https://raw.githubusercontent.com/securisec/chepy/master/logo.png" width="65%">
</p>

![](https://github.com/securisec/chepy/workflows/tests/badge.svg)
<!-- ![](https://img.shields.io/travis/com/securisec/chepy?logo=travis) -->
<!-- [![](https://img.shields.io/docker/cloud/build/securisec/chepy?logo=docker)](https://hub.docker.com/r/securisec/chepy) -->

[![](https://img.shields.io/readthedocs/chepy.svg?logo=read-the-docs&label=Docs)](http://chepy.readthedocs.io/en/latest/)
[![](https://img.shields.io/pypi/v/chepy.svg?logo=pypi&label=pypi)](https://pypi.python.org/pypi/chepy)

[![](https://codecov.io/gh/securisec/chepy/branch/master/graph/badge.svg?token=q3pRktSVBu)](https://codecov.io/gh/securisec/chepy)

[![](https://img.shields.io/badge/code%20style-black-000000.svg?label=Style)](https://github.com/securisec/chepy)
![](https://img.shields.io/github/license/securisec/chepy?label=License)

[![](https://pepy.tech/badge/chepy)](https://pepy.tech/project/chepy)
<!-- ![](https://img.shields.io/docker/pulls/securisec/chepy?label=Docker%20pull&logo=docker) -->


# Chepy


![Solving a CTF with Chepy](https://raw.githubusercontent.com/securisec/chepy/master/docs/assets/ctf.gif)

Chepy is a python library with a handy cli that is aimed to mirror some of the capabilities of [CyberChef](https://gchq.github.io/CyberChef/). A reasonable amount of effort was put behind Chepy to make it compatible to the various functionalities that CyberChef offers, all in a pure Pythonic manner. There are some key advantages and disadvantages that Chepy has over Cyberchef. The Cyberchef concept of _stacking_ different modules is kept alive in Chepy.

There is still a long way to go for Chepy as it does not offer every single ability of Cyberchef.

## Feel free to give the project a ⭐️!

## Docs
[Refer to the docs for full usage information](http://chepy.readthedocs.io/en/latest/)

## Example
[For all usage and examples, see the docs.](http://chepy.readthedocs.io/en/latest/)

Chepy has a stacking mechanism similar to Cyberchef. For example, this in Cyberchef:

<img src="https://raw.githubusercontent.com/securisec/chepy/master/docs/assets/cc_encoding.png" width=400px>

This is equivalent to 

```python
from chepy import Chepy

file_path = "/tmp/demo/encoding"

print(
    Chepy(file_path)
    .load_file()
    .reverse()
    .rot_13()
    .from_base64()
    .from_base32()
    .hexdump_to_str()
    .o
)

```

## Chepy vs Cyberchef

#### Advantages
- Chepy is pure python with a supporting and accessible python api
- Chepy has a CLI
- Chepy CLI has full autocompletion.
- Supports pe, elf, and other various file format specific parsing.  
- Extendable via [plugins](https://chepy-plugins.readthedocs.io/en/latest/)
- Infinitely scalable as it can leverage the full Python library.
- Chepy can interface with the full Cyberchef web app to a certain degree. It is easy to move from Chepy to Cyberchef if need be. 
- The Chepy python library is significantly faster than the Cyberchef Node library.
- Works with HTTP/S requests without CORS issues.
- `magic` support via the Chepy ML plugin.

#### Disadvantages
- Chepy does not offer every single thing that Cyberchef does


## Installation
Chepy can be installed in a few ways.

### Pypi
```bash
pip3 install chepy
# optionally with extra requirements
pip3 install chepy[extras]
```

### Git
```bash
git clone --recursive https://github.com/securisec/chepy.git
cd chepy
pip3 install -e .
# I use -e here so that if I update later with git pull, I dont have it install it again (unless dependencies have changed)
```

<!-- #### [Docker](https://hub.docker.com/r/securisec/chepy)
```bash
docker run --rm -ti -v $PWD:/data securisec/chepy "some string" [somefile, "another string"]
``` -->

#### Standalone binary
One can build Chepy to be a standalone binary also. This includes packaging all the dependencies together.
```bash
git clone https://github.com/securisec/chepy.git
cd chepy
pip install .
pip install pyinstaller
pyinstaller cli.py --name chepy --onefile
```
The binary will be in the dist/ folder. 

### Plugins
[Check here for plugins docs](https://chepy-plugins.readthedocs.io/en/latest/)

### Used by
[Remnux linux](https://docs.remnux.org/discover-the-tools/examine+static+properties/deobfuscation#chepy)

```eval_rst
.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage.md
   examples.md
   cli.rst
   chepy.md
   core.md
   modules.rst
   extras.rst
   plugins.md
   pullrequest.md
   config.md
   faq.md


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```
