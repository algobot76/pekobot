import logging
import os
import random

from discord import File
from discord.ext import commands

from pekobot.bot import Bot
from pekobot.utils import checks

logger = logging.getLogger(__name__)


class Setu(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.setu_path = os.path.join("images", "setu")

    @commands.command(name="setu", aliases=("色图", "涩图"))
    @checks.is_nsfw()
    async def send_setu(self, ctx: commands.Context):
        author = ctx.author
        logger.info(f"{author} is requesting a setu.")
        setu_images = os.listdir(self.setu_path)
        selected_image = random.choice(setu_images)
        await ctx.send(file=File(os.path.join(self.setu_path, selected_image)))


def setup(bot):
    bot.add_cog(Setu(bot))
