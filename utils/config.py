import yaml


def load_config(config_path="pekobot-config.yaml"):
    with open(config_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    token = data["discord_token"]
    cogs = data["cogs"]
    ignored_channels = data["ignored_channels"]
    pixiv_username = data["pixiv"]["username"]
    pixiv_password = data["pixiv"]["password"]

    return dict(discord_token=token,
                ignored_channels=ignored_channels,
                pixiv_username=pixiv_username,
                pixiv_password=pixiv_password,
                cogs=cogs)
