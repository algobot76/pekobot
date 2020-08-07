# pylint: skip-file
from discord.ext import commands
from pixivpy3 import AppPixivAPI

from pekobot.utils import config


class Pixiv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        conf = config.load_config()
        self.api = AppPixivAPI()
        self.api.login(conf["pixiv_username"], conf["pixiv_password"])

    @commands.command(name="Pixiv", aliases=("pixiv", "PIXIV"))
    async def pixiv(self, ctx, option):
        mode = ""
        if option == "推荐":
            mode = "day"
        elif option == "色图" or option == "涩图" or option == "setu":
            mode = "day_r18"

        result = self.api.illust_ranking(mode)
        illusts = result.illusts[:10]
        for illust in illusts:
            await ctx.send(
                f"{illust.title} - https://www.pixiv.net/artworks/{illust.id}")
        else:
            await ctx.send(f"未知选项：{option}")


def setup(bot):
    bot.add_cog(Pixiv(bot))
