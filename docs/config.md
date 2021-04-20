# Config

Chepy is set to look at the present working directory for a a folder called **.chepy** for config files. By default, Chepy config files are stored in a folder called **.chepy** in the users home directory. There are two files in it. 

If any of the config options are missing, Chepy will automatically assign default values to it. If **.chepy** folder is detected, but config options have been set, then Chepy will automatically create a set of default config options.

## chepy.conf
### Plugin.enableplugins
This should be set to either `true` or `false` to control if plugins should be loaded by Chepy.
### Plugin.pluginpath
This path controls where chepy will look for plugins and extensions. For more information, see [plugins](/plugins)

### Cli.history_path
Path where the chepy cli history is stored. Defaults to *USERHOME/.chepy/chepy_history*
### Cli.prompt_colors
Controls the colors of **>>>** in chepy prompt. Should be space seperated 3 hex color codes. Defaults to *#00ffff #ff0000 #ffd700*
### Cli.show_rprompt
Controls visibility of the right prompt. Value should be *true* or *false*. Defaults to *false*.
### Cli.prompt_rprompt
Controls the colors of of the right prompt. Defaults to *#00ff48*
### Cli.prompt_bottom_toolbar
Controls the color of the bottom toolbar. Defaults to *#000000*
### Cli.prompt_toolbar_version
Controls the color of the version in the toolbar. Defaults to *#00ff48*
### Cli.prompt_toolbar_states
Controls the color of the states in the toolbar. Defaults to *#60cdd5*
### Cli.prompt_toolbar_buffers
Controls the color of the buffers in the toolbar. Defaults to *#ff00ff*
### Cli.prompt_toolbar_type
Controls the color of the current state type in the toolbar. Defaults to *#ffd700*
### Cli.prompt_toolbar_errors
Controls the color of the errors in the toolbar. Defaults to *#ff0000*
### Cli.prompt_cli_method
Controls the color of the cli methods. Defaults to *#00d700*
### Cli.prompt_plugin_method
Controls the color of the plugin methods. Defaults to *#30d8ff*
### Cli.cli_info_color
Controls the color of the output from `cli_*` methods. Defaults to *#ffb4ad*
### Cli.prompt_search_background
Background background color for cli selection. Defaults to *#00aaaa #000000*
### Cli.prompt_search_fuzzy
Background background color for cli fuzzy match. Defaults to *#00aaaa*


### chepy_history
This file saves the history of all the commands in that have been run in the chepy cli. 

### Valid chepy.conf file contents
```
[Plugins]
enableplugins = false
pluginpath = /path/to/chepy_install/chepy/chepy/chepy_plugins

[Cli]
history_path = /path/to/home/.chepy/chepy_history
prompt_char = >
prompt_colors = #00ffff #ff0000 #ffd700
show_rprompt = false
prompt_rprompt = #00ff48
prompt_bottom_toolbar = #000000
prompt_toolbar_version = #00ff48
prompt_toolbar_states = #60cdd5
prompt_toolbar_buffers = #ff00ff
prompt_toolbar_type = #ffd700
prompt_toolbar_errors = #ff0000
```
