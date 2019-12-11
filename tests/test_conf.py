from pathlib import Path
from chepy.config import ChepyConfig


def test_config():
    config = ChepyConfig()
    config_dir = Path.home() / ".chepy"
    assert config.history_path == str(config_dir / "chepy_history")
    assert str(config.chepy_conf) == str(config_dir / "chepy.conf")
    assert Path(config.chepy_conf).exists()
    assert Path(config.history_path).exists()
    assert config.prompt_bottom_toolbar.startswith("#")
    assert config.prompt_rprompt.startswith("#")
    assert config.prompt_toolbar_buffers.startswith("#")
    assert config.prompt_toolbar_errors.startswith("#")
    assert config.prompt_toolbar_states.startswith("#")
    assert config.prompt_toolbar_type.startswith("#")
    assert config.prompt_toolbar_version.startswith("#")
    assert config.prompt_char is not None
    assert len(config.prompt_colors.split()) == 3
