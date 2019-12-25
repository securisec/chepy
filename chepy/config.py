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
        self.chepy_dir = Path(home / ".chepy")
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
            cli_options["prompt_toolbar_errors"] = "#ff0000"

            Path(str(self.chepy_dir / "chepy_history")).touch()
            if not self.chepy_conf.exists():
                with open(str(self.chepy_conf), "w") as f:
                    c.write(f)

        self.config = ConfigParser()
        self.config.read(str(self.chepy_conf))

        plugin_path = self.config["Plugins"]["PluginPath"]
        self.enable_plugins = json.loads(self.config["Plugins"]["EnablePlugins"])

        if self.enable_plugins:
            if plugin_path != "None":
                self.plugin_path = Path(plugin_path).expanduser().resolve()
            else:
                self.plugin_path = Path(plugin_path)
        else:
            self.plugin_path = Path("None")

        self.history_path = self.config["Cli"]["history_path"]
        self.prompt_char = self.config["Cli"]["prompt_char"]
        self.prompt_colors = self.config["Cli"]["prompt_colors"]
        self.show_rprompt = json.loads(self.config["Cli"]["show_rprompt"])
        self.prompt_rprompt = self.config["Cli"]["prompt_rprompt"]
        self.prompt_bottom_toolbar = self.config["Cli"]["prompt_bottom_toolbar"]
        self.prompt_toolbar_version = self.config["Cli"]["prompt_toolbar_version"]
        self.prompt_toolbar_states = self.config["Cli"]["prompt_toolbar_states"]
        self.prompt_toolbar_buffers = self.config["Cli"]["prompt_toolbar_buffers"]
        self.prompt_toolbar_type = self.config["Cli"]["prompt_toolbar_type"]
        self.prompt_toolbar_errors = self.config["Cli"]["prompt_toolbar_errors"]

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
                    logging.warning("Error loading {}".format(plugin.__name__))
        return plugins
