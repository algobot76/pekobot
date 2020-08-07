"""A module that contains config-related functions."""
from typing import List, TypedDict

import yaml


class Conf(TypedDict):
    """Representation of Pekobot configuration."""
    discord_token: str
    pixiv_username: str
    pixiv_password: str
    cogs: List[str]


def load_config(config_path: str = "pekobot-config.yaml") -> Conf:
    """Loads the Pekobot config.

       Args:
           config_path: File path to the config file.

       Returns:
           A dict that contains the content of the config.
    """

    with open(config_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    token = data["discord_token"]
    cogs = data["cogs"]
    pixiv_username = data["pixiv"]["username"]
    pixiv_password = data["pixiv"]["password"]

    return dict(discord_token=token,
                pixiv_username=pixiv_username,
                pixiv_password=pixiv_password,
                cogs=cogs)
