import logging
import os
import random

import discord
from discord.ext import commands

NYB_TEXT = '''
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''

logger = logging.getLogger(__name__)


class Peko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        PEKO_ID = 105801  # 105801 is the unit id of ペコリーヌ
        query = f'''
        SELECT description FROM unit_comments
        WHERE unit_id={PEKO_ID}
        '''
        cursor = self.bot.pcr_db.cursor()
        cursor.execute(query)
        self.comments = []
        for comment, in cursor.fetchall():
            comment = comment.replace("\\n", "")
            self.comments.append(comment)

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
            await msg.channel.send(file=discord.File(
                os.path.join("pekobot", "cogs", "data", "nyb.gif")))
            await msg.channel.send(NYB_TEXT)

    @commands.command(name="tap", aliases=("戳", "👇"))
    async def send_random_comment(self, ctx: discord.ext.commands.Context):
        logger.info(f"Pekobot has been tapped by {ctx.author}.")
        comment = random.choice(self.comments)
        await ctx.send(comment)

    @commands.command(name="status", aliases=("状态", ))
    async def status(self, ctx: discord.ext.commands.Context):
        logger.info(f"Pekobot's status has been queried by {ctx.author}.")
        setu_dir = os.path.join("images", "setu")
        setu_count = count_files(setu_dir)
        setu_status = f"目前涩图数量：{setu_count}\n"
        header = "状态报告：\n\n"
        report = header + setu_status
        await ctx.send(report)


def setup(bot):
    bot.add_cog(Peko(bot))


def count_files(dir):
    count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            count += 1
    return count
