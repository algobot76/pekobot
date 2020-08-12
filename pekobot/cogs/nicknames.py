"""Nicknames cog"""
import os

from discord.ext import commands

from pekobot.utils import files

NICKNAMES_FILE_PATH = os.path.join("data", "nicknames.yaml")


class Nicknames(commands.Cog, name="昵称插件"):
    """The Nicknames cog.

    Attributes:
        bot: A Pekobot instance.
        data: Data of nicknames.
    """
    def __init__(self, bot):
        self.bot = bot
        self.data = files.load_yaml_file(NICKNAMES_FILE_PATH)

    @commands.command(name="whois", aliases=("谁是", ))
    async def whois(self, ctx, nickname):
        """通过昵称查找角色。"""

        for _, v in self.data.items():
            if nickname in v["nicknames"]:
                await ctx.send(
                    f"{v['cn_name']} (繁：{v['tc_name']}，日：{v['jp_name']})")
            else:
                await ctx.send("不认识的孩子呢～～～")


def setup(bot):
    """A helper function used to load the Nicknames cog."""

    bot.add_cog(Nicknames(bot))
