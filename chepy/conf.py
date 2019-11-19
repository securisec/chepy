import json
from pathlib import Path
from configparser import ConfigParser


class Config(object):
    def __init__(self):
        home = Path.home()
        self.chepy_dir = Path(home / ".chepy")
        self.chepy_conf = Path(self.chepy_dir / "chepy.conf")

        self.config = ConfigParser()
        self.config.read(str(self.chepy_conf))

        self.plugin_path = self.config["Plugin"]["PluginPath"]

        self.history_path = self.config["Cli"]["HistoryPath"]
