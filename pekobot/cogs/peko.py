"""Peko cog"""
import logging
import os
import random

import discord
from discord.ext import commands

from pekobot.pekobot import Pekobot

NYB_TEXT = '''
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''

logger = logging.getLogger(__name__)


class Peko(commands.Cog, name="佩可插件"):
    """The Peko cog.

    Attributes:
        bot: A Pekobot instance.
        comments: A list of comments by ペコリーヌ.
    """
    def __init__(self, bot):
        self.bot = bot

        PEKO_ID = 105801  # 105801 is the unit id of ペコリーヌ
        query = f'''
        SELECT description FROM unit_comments
        WHERE unit_id={PEKO_ID}
        '''
        conn = self.bot.g.get("pcr_db")
        cursor = conn.cursor()
        cursor.execute(query)
        self.comments = []
        for comment, in cursor.fetchall():
            comment = comment.replace("\\n", "")
            self.comments.append(comment)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Triggered when a new member joined the server.

        Args:
            member: a discord member.
        """

        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('等你好久了 {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context,
                               error: commands.CommandError):
        """Triggered when there is a command error.

        Args:
            ctx: A command context.
            error: A command error.
        """

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("老娘不认识的指令呢～～")
            return
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("你在想啥呢？变态ヽ(`⌒´メ)ノ")
            return
        if isinstance(error, commands.MissingPermissions):
            if "administrator" in error.missing_perms:
                await ctx.send("此功能只对管理员开放")
                return
        raise error

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Triggered when there is a new message.

        Args:
            msg: A new message.
        """

        if "春黑" in msg.content:
            await msg.channel.send(file=discord.File(
                os.path.join("pekobot", "cogs", "data", "nyb.gif")))
            await msg.channel.send(NYB_TEXT)

    @commands.command(name="tap", aliases=("戳", "👇"))
    async def send_random_comment(self, ctx: commands.Context):
        """让佩可说出一个随机台词。"""

        logger.info("Pekobot has been tapped by %s.", ctx.author)
        comment = random.choice(self.comments)
        await ctx.send(comment)

    @commands.command(name="status", aliases=("状态", ))
    async def status(self, ctx: discord.ext.commands.Context):
        """查看机器人状态。"""

        logger.info("Pekobot's status has been queried by %s.", ctx.author)
        setu_dir = os.path.join("images", "setu")
        setu_count = count_files(setu_dir)
        setu_status = f"目前涩图数量：{setu_count}\n"
        header = "状态报告\n\n"
        report = header + setu_status
        await ctx.send(report)


def setup(bot: Pekobot):
    """A helper function used to load the cog."""

    bot.add_cog(Peko(bot))


def count_files(dir_path):
    """Counts the number of files in a directory.

    Args:
        dir_path: A directory path.
    """

    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count
