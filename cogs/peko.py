from discord.ext import commands


class Peko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("老娘不认识的指令呢～～")
            return
        raise error


def setup(bot):
    bot.add_cog(Peko(bot))
