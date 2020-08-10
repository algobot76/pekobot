"""An extension of commands.Bot"""
import aiohttp
from discord.ext import commands


class Pekobot(commands.Bot):
    """Representation of Pekobot.

    Attributes:
        session: A client session of aiohttp.
        g: A custom context dict.
    """
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop("command_prefix"))
        self.session = aiohttp.ClientSession(loop=self.loop)

        self.g = dict()  # inspired by flask.g
        self.g["pcr_db"] = kwargs.pop("pcr_db")

        self.remove_command("help")
