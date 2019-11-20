# Chepy Class

The **Chepy** class in the main class for Chepy, and includes all the methods from all the different classes under modules. This class takes ***args** as its argument, and each argument that is passed to it becomes its own state. 

```python
>>> from chepy import Chepy
>>> c = Chepy("some data", "/some/path/file")
>>> c.states
{0: "some data", 1: "/some/path/file"}
```

```eval_rst
.. autoclass:: chepy.Chepy
    :members:
    :inherited-members:

    .. automethod:: __init__
```