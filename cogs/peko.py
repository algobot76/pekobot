import os

import discord
from discord.ext import commands

NYB_TEXT = '''
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''


class Peko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('等你好久了 {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("老娘不认识的指令呢～～")
            return
        raise error

    @commands.Cog.listener()
    async def on_message(self, msg):
        if "春黑" in msg.content:
            await msg.channel.send(
                file=discord.File(os.path.join("cogs", "data", "nyb.gif")))
            await msg.channel.send(NYB_TEXT)


def setup(bot):
    bot.add_cog(Peko(bot))
