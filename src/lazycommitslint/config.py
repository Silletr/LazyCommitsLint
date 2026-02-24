# import tomlkit
# Config's will be contain on ~/lcl_config.toml for convenience

from pathlib import Path

config_file = "~/lcl_config.toml"


def create_config():
    config_file = Path.home() / "lcl_config.toml"
    with open(config_file, mode="w") as config:
        config.write(
            "!!! JUST FOR A TEST,"
            "FROM LazyCommitsLint/src/lazycommitslint/config.py, 9 string"
            "!!!"
        )


def read_config():
    with open(config_file, mode="r") as config:
        config.read()


create_config()
