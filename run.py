# pylint: skip-file
import asyncio
import logging
import os

import aiohttp
import brotli

from pekobot.bot import Bot
from pekobot.utils import config
from pekobot.utils import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('pekobot')

conf = config.load_config()


async def run():
    # Download redive_jp.db from https://redive.estertion.win/ if it doesn't exist
    if not os.path.exists("redive_jp.db"):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://redive.estertion.win/db/redive_jp.db.br") as resp:
                brotli_result = await resp.read()
                data = brotli.decompress(brotli_result)
                with open("redive_jp.db", "wb") as f:
                    f.write(data)

    pcr_db = db.create_connection("redive_jp.db")
    bot = Bot(command_prefix=("!", "！"), pcr_db=pcr_db)
    for cog in conf["cogs"]:
        bot.load_extension(f"pekobot.cogs.{cog}")

    @bot.event
    async def on_ready():
        logger.info(f'{bot.user} has connected to Discord!')

    try:
        await bot.start(conf['discord_token'])
    except KeyboardInterrupt:
        pcr_db.close()
        await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
