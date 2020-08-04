import asyncio

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

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    @bot.event
    async def on_message(msg):
        name = msg.channel.name
        if name in conf["ignored_channels"]:
            return

    try:
        await bot.start(conf['discord_token'])
    except KeyboardInterrupt:
        conn.close()
        await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
