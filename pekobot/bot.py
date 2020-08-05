import aiohttp
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop("command_prefix"))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.pcr_db = kwargs.pop("pcr_db")
