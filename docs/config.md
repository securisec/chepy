# Config

The Chepy config files are stored in a folder called **.chepy** in the users home directory. There are two files in it. 

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


### chepy_history
This file saves the history of all the commands in that have been run in the chepy cli. 