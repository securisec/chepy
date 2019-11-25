<img src="https://raw.githubusercontent.com/securisec/chepy/master/logo.png" width="150px">

![](https://github.com/securisec/chepy/workflows/tests/badge.svg)
[![](https://img.shields.io/travis/securisec/chepy.svg?label=Travis&logo=travis&branch=master)](https://travis-ci.com/securisec/chepy)
[![](https://codecov.io/gh/securisec/chepy/branch/master/graph/badge.svg?token=q3pRktSVBu)](https://codecov.io/gh/securisec/chepy)

[![](https://img.shields.io/readthedocs/chepy.svg?logo=read-the-docs&label=Docs)](http://chepy.readthedocs.io/en/latest/)
[![](https://img.shields.io/pypi/v/chepy.svg?logo=pypi&label=pypi)](https://pypi.python.org/pypi/chepy)

[![](https://img.shields.io/badge/code%20style-black-000000.svg?label=Style)](https://github.com/securisec/chepy)
![](https://img.shields.io/pypi/l/chepy?label=license)


# Chepy

![Solving a CTF with Chepy](https://raw.githubusercontent.com/securisec/chepy/master/docs/assets/ctf.gif)

Chepy is a python library with a handy cli that is aimed to mirror some of the capabilities of [CyberChef](https://gchq.github.io/CyberChef/). A reasonable amount of effort was put behind Chepy to make it compatible to the various functionalities that CyberChef offers, all in a pure Pythonic manner. There are some key advantages and disadvantages that Chepy has over Cyberchef. The Cyberchef concept of _stacking_ different modules is kept alive in Chepy.

There is still a long way to go for Chepy as it does not offer every single ability of Cyberchef.

## Docs
[Refer to the docs for full usage information](http://chepy.readthedocs.io/en/latest/)

## Installation
Chepy can be installed in a few ways.

### Pypi
```bash
pip3 install chepy
```

### Git
```bash
git clone https://github.com/securisec/chepy.git
cd chepy
pip3 install -e .
# I use -e here so that if I update later with git pull, I dont have it install it again (unless dependencies have changed)
```

#### Pipenv
```
git clone https://github.com/securisec/chepy.git
cd chepy
pipenv install
```

## Chepy vs Cyberchef

#### Advantages
- Chepy is pure python with a supporting and accessible python api
- Chepy has a CLI
- Chepy CLI has full autocompletion. 
- Extendable via plugins
- Infinitely scalable as it can leverage the full Python library.
- Chepy can interface with the full Cyberchef web app to a certain degree. It is easy to move from Chepy to Cyberchef if need be. 
- The Chepy python library is significantly faster than the Cyberchef Node library.
- Works with HTTP/S requests without CORS issues.

#### Disadvantages
- Chepy is not a web app (at least for now).
- Chepy does not offer every single thing that Cyberchef does
- Chepy does not have the `magic` method (at the moment)



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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```