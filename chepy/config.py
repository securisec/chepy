import sys
import logging
import importlib
import inspect
import pkgutil
import json
from pathlib import Path
from configparser import ConfigParser


class ChepyConfig(object):
    def __init__(self):
        home = Path.home()
        self.chepy_dir = (
            Path(".chepy").resolve()
            if Path(".chepy").exists()
            else Path(home / ".chepy")
        )
        self.chepy_conf = Path(self.chepy_dir / "chepy.conf")

        if not self.chepy_conf.exists():  # pragma: no cover
            self.chepy_dir.mkdir(exist_ok=True)
            c = ConfigParser()

            c["Plugins"] = {
                "EnablePlugins": "false",
                "PluginPath": str(Path(__file__).parent / "chepy_plugins"),
            }
            c["Cli"] = {}
            cli_options = c["Cli"]
            cli_options["history_path"] = str(self.chepy_dir / "chepy_history")
            cli_options["prompt_char"] = ">"
            cli_options["prompt_colors"] = "#00ffff #ff0000 #ffd700"
            cli_options["show_rprompt"] = "false"
            cli_options["prompt_rprompt"] = "#00ff48"
            cli_options["prompt_bottom_toolbar"] = "#000000"
            cli_options["prompt_toolbar_version"] = "#00ff48"
            cli_options["prompt_toolbar_states"] = "#60cdd5"
            cli_options["prompt_toolbar_buffers"] = "#ff00ff"
            cli_options["prompt_toolbar_type"] = "#ffd700"
            cli_options["prompt_toolbar_plugins"] = "#ffccbc"
            cli_options["prompt_toolbar_errors"] = "#ff0000"
            cli_options["prompt_cli_method"] = "#ffd700"
            cli_options["prompt_plugin_method"] = "#30d8ff"
            cli_options["cli_info_color"] = "#c2c2ff"
            cli_options["prompt_search_background"] = "#00aaaa #000000"
            cli_options["prompt_search_fuzzy"] = "#00aaaa"

            Path(str(self.chepy_dir / "chepy_history")).touch()
            if not self.chepy_conf.exists():
                with open(str(self.chepy_conf), "w") as f:
                    c.write(f)

        self.config = ConfigParser()
        self.config.read(str(self.chepy_conf))

        plugin_path = self.__get_conf_value("None", "PluginPath", "Plugins")
        self.enable_plugins = json.loads(
            self.__get_conf_value("false", "EnablePlugins", "Plugins")
        )

        if self.enable_plugins:
            if plugin_path != "None":
                self.plugin_path = Path(plugin_path).expanduser().resolve()
            else:
                self.plugin_path = Path(plugin_path)
        else:
            self.plugin_path = Path("None")

        self.history_path = self.__get_conf_value(
            str(self.chepy_dir / "chepy_history"), "history_path"
        )
        self.prompt_char = self.__get_conf_value(">", "prompt_char")
        self.prompt_colors = self.__get_conf_value(
            "#00ffff #ff0000 #ffd700", "prompt_colors"
        )
        self.show_rprompt = json.loads(self.__get_conf_value("false", "show_rprompt"))
        self.prompt_rprompt = self.__get_conf_value("#00ff48", "prompt_rprompt")
        self.prompt_bottom_toolbar = self.__get_conf_value(
            "#000000", "prompt_bottom_toolbar"
        )
        self.prompt_toolbar_version = self.__get_conf_value(
            "#00ff48", "prompt_toolbar_version"
        )
        self.prompt_toolbar_states = self.__get_conf_value(
            "#60cdd5", "prompt_toolbar_states"
        )
        self.prompt_toolbar_buffers = self.__get_conf_value(
            "#ff00ff", "prompt_toolbar_buffers"
        )
        self.prompt_toolbar_type = self.__get_conf_value(
            "#ffd700", "prompt_toolbar_type"
        )
        self.prompt_toolbar_plugins = self.__get_conf_value(
            "#ffccbc", "prompt_toolbar_plugins"
        )
        self.prompt_toolbar_errors = self.__get_conf_value(
            "#ff0000", "prompt_toolbar_errors"
        )
        self.prompt_search_background = self.__get_conf_value(
            "#00aaaa #000000", "prompt_search_background"
        )
        self.prompt_search_fuzzy = self.__get_conf_value(
            "#00aaaa", "prompt_search_fuzzy"
        )
        self.prompt_cli_method = self.__get_conf_value("#ffd700", "prompt_cli_method")
        self.prompt_plugin_method = self.__get_conf_value(
            "#30d8ff", "prompt_plugin_method"
        )
        self.cli_info_color = self.__get_conf_value("#c2c2ff", "cli_info_color")

    def __get_conf_value(self, default: str, option: str, section: str = "Cli"):
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config[section][option]
            else:
                return default
        else:
            return default

    def load_plugins(self):  # pragma: no cover
        plugins = []
        if self.plugin_path.stem != "None":
            sys.path.append(str(self.plugin_path))

            my_plugins = [
                importlib.import_module(name)
                for finder, name, ispkg in pkgutil.iter_modules()
                if (name.startswith("chepy_") and name != "chepy_plugins")
            ]

            for plugin in my_plugins:
                try:
                    klass, mod = inspect.getmembers(plugin, inspect.isclass)[0]
                    loaded = getattr(plugin, klass)
                    plugins.append(loaded)
                except:
                    logging.warning(f"Error loading {plugin.__name__}")
        return plugins
