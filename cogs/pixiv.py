import os

from discord.ext import commands
from pixivpy3 import AppPixivAPI

from utils import config


class Pixiv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        conf = config.load_config()
        self.api = AppPixivAPI()
        self.api.login(conf["pixiv_username"], conf["pixiv_password"])

    @commands.command(name="Pixiv", aliases=("pixiv", "PIXIV"))
    async def pixiv(self, ctx, option):
        if option == "推荐":
            result = self.api.illust_ranking('day')
            illusts = result.illusts[:10]
            for illust in illusts:
                await ctx.send(
                    f"{illust.title} - https://www.pixiv.net/artworks/{illust.id}"
                )
        else:
            await ctx.send(f"未知选项：{option}")


def setup(bot):
    bot.add_cog(Pixiv(bot))
