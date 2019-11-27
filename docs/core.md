# ChepyCore class

The `ChepyCore` class for Chepy is primarily used as an interface for all the current modules/classes in Chepy, or for plugin development. The `ChepyCore` class is what provides the various attributes like **states**, **buffers**, etc and is required to use and extend Chepy.

The most important `ChepyCore` attributes and methods are:
- **state** The state is where all objects are always stored when modified by any methods. 
- **\_convert_to_*** methods These are helper methods that ensures data is being accessed and put in the state in the correct manner. For example, `binasii.unhexlify` requires a bytes like object. We can use 
```
self.state = binasii.unhexlify(self._convert_to_bytes())
```
This will ensure that the correct data type is being used at all times.

```eval_rst
.. automodule:: chepy.core
    :members:
    :undoc-members:
    :private-members:
```
