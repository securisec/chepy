# Chepy Plugins

Chepy allows users to extend Chepy and add plugins to it. This documentation describes how to create or load plugins in Chepy.

## chepy.conf file
The chepy.conf file is what controls various aspects of how chepy runs. This file can be located in the users home directory. 

The default Chepy conf file on setup looks like this:

```bash
[Plugin]
pluginpath = None
# this needs to be an absolute path. Plugins are loaded from this directory

[Cli]
historypath = /home/hapsida/.chepy/chepy_history
# controls where the Chepy cli history is saved. This path will be set to
# the users home dir automatically on setup.
```

## Plugins folder location
The location of the plugins folder can be found in the `chepy.conf` file. To use custom plugins, set the value of `pluginpath` in this file.

```bash
[Plugin]
pluginpath = /some/dir/
```

Chepy will attempt to read the plugins folder (if one is set) to resolve any plugins from it. 

## Creating plugins
### Naming plugins
Because Chepy utilizes name spaces to load its plugins, all plugin files needs to be named as **chepy_some_plugin.py**. This ensures that there are no namespace conflicts. 

Plugin files should be placed in the directory that is specified by the `pluginpath` in chepy.conf
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
### Plugin module
All Chepy plugins have to follow a specific format for best results. 

- ChepyCore needs to be inherited in the plugin class
- Methods must have [google style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- Methods should preferably be prefixed with something that distinguishes them. For example `myplugin_somemethod`. This avoids namespace conflicts. 

### Sample plugin
![Plugin](./assets/plugin.gif)
[Asciinema](https://asciinema.org/a/apIR9AWO3EZpHrfKYfagVZk06)

This is a bare bones example of how a Chepy plugin works. In this case, `myplugin_method` will be available in both Chepy cli (with auto completion) and the Chepy library.

The only thing this plugin at the moment will do is take whatever value is in the state, and multiply it with 20. All methods in Chepy plugins should set the value of `self.state` and should return `self`. This allows chaining with other methods that are available. 

```python
import chepy
from chepy.core import ChepyDecorators

class MyPlugin(chepy.core.ChepyCore):
    
    @ChepyDecorators.call_stack
    def myplugin_method(self):
        """another method
        
        Returns:
            Chepy: The chepy object
        """
        self.state = self.state * 20
        return self
```

Lets breakdown this sample plugin.

#### Importing ChepyCore

```python
import chepy
from chepy.core import ChepyDecorators

class MyPlugin(chepy.core.ChepyCore):

    @ChepyDecorators.call_stack
    def myplugin_method(self):
```
All Chepy plugins needs to inherit the **ChepyCore** class. This ensures that all the core attributes and methods from ChepyCore are available to the plugin.

The **ChepyDecorators** class offers stack methods to decorate plugin methods with. In this example, the `call_stack` decorator is being applied to the `myplugin_method` method. Although using the decorator is not required, it is recommended. This decorator ensures that that external plugins are also able to use the recipe feature. 

#### Docstrings
```python
"""another method
        
Returns:
    Chepy: The chepy object
"""
```

This is an example of Google style docstrings in python. Chepy cli parses these doc strings to show the help message and command completion dynamically. Although this can be omitted, it is strong recommended to have them to leverage the best capabilities of Chepy. 

#### Method body
This could be any code that the method is trying to accomplish

#### Returns
```python
self.state = self.state * 20
return self
```
```eval_rst
.. important::
    These two lines are very important. Both Chepy cli and library allows the user to chain various methods with each other. 
```

- `self.state = ...` This line ensures that the value being produced by the method can be accessed by other methods in Chepy.
- `return self` This line ensures that methods can be changed together. Example, 

In the example gif and asciinema, we can see how we first load the hello string to chepy, then call our myplugin_method, and then modify the output with to_hex followed by base64_encode.

#### Using plugins in script
As all plugins found in the directory is loaded automatically by Chepy at init, using plugins in script is super simple. 

This code is equivalent to what is happening in the gif and asciinema. 

```python
from chepy import Chepy

c = Chepy("hello").myplugin_method().to_hex().base64_encode()
print(c)
```

```eval_rst
.. tip::
    If you do create a plugin that is helpful, feel free to share it, or make a pull request!   
```
