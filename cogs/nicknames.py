import yaml

from discord.ext import commands

NICKNAMES_FILE_PATH = "cogs/data/nicknames.yaml"


class Nicknames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(NICKNAMES_FILE_PATH, "r") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    @commands.command(name="谁是")
    async def whois(self, ctx, nickname):
        for k, v in self.data.items():
            if nickname in v["nicknames"]:
                await ctx.send(
                    f"{v['cn_name']} (繁：{v['tc_name']}，日：{v['jp_name']})")
            else:
                await ctx.send("不认识的孩子呢～～～")


def setup(bot):
    bot.add_cog(Nicknames(bot))
