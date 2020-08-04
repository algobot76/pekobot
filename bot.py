import asyncio
import os

import aiohttp
import brotli
from discord.ext import commands

from utils import config
from utils import db


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop("command_prefix"))

        self.db_conn = kwargs.pop("db_conn")


conf = config.load_config()


async def run():
    conn = db.create_connection("pekobot.db")
    bot = Bot(command_prefix=("!", "！"), db_conn=conn)
    for cog in conf["cogs"]:
        bot.load_extension(cog)

    # Download redive_jp.db from https://redive.estertion.win/ if it doesn't exist
    if not os.path.exists("redive_jp.db"):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://redive.estertion.win/db/redive_jp.db.br") as resp:
                brotli_result = await resp.read()
                data = brotli.decompress(brotli_result)
                with open("redive_jp.db", "wb") as f:
                    f.write(data)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    try:
        await bot.start(conf['discord_token'])
    except KeyboardInterrupt:
        conn.close()
        await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
