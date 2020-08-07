"""Setu cog"""
import logging
import os
import random

from discord import File
from discord.ext import commands

from pekobot.bot import Bot

logger = logging.getLogger(__name__)

SETU_PATH = os.path.join("images", "setu")


class Setu(commands.Cog, name="色图插件"):
    """The Setu cog

    Attributes:
        bot: A Pekobot instance.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="setu", aliases=("色图", "涩图"))
    @commands.is_nsfw()
    async def send_setu(self, ctx: commands.Context):
        """来一份色图。"""

        author = ctx.author
        logger.info("%s is requesting a setu.", author)
        setu_images = os.listdir(SETU_PATH)
        selected_image = random.choice(setu_images)
        await ctx.send(file=File(os.path.join(SETU_PATH, selected_image)))


def setup(bot):
    """A helper fuction used to load the cog."""

    bot.add_cog(Setu(bot))
