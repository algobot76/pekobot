import os
import random

import discord
from discord.ext import commands


class Setu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setu_path = os.path.join("images", "setu")

    @commands.command(name="setu", aliases=("Setu", "色图", "涩图"))
    @commands.is_nsfw()
    async def send_setu(self, ctx):
        setu_images = os.listdir(self.setu_path)
        num = random.randint(0, len(setu_images))
        if num == 0:
            await ctx.send("我已经被榨干了，呜～～")
        else:
            await ctx.send(file=discord.File(
                os.path.join(self.setu_path, setu_images[num - 1])))


def setup(bot):
    bot.add_cog(Setu(bot))
