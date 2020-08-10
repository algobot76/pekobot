"""An extension of commands.Bot"""
import logging

import aiohttp
from discord.ext import commands

logger = logging.getLogger(__name__)


@commands.command(name="help", aliases=("帮助", ))
async def help_(ctx: commands.Context):
    """查看使用说明"""

    logger.info("%s (%s) is asking for help.", ctx.author, ctx.guild)

    cogs = [cog for _, cog in ctx.bot.cogs.items()]

    manual = "使用说明\n"
    manual += "=======\n"

    for cog in cogs:
        cog_name = cog.qualified_name
        manual += f"{cog_name}：\n"

        commands_ = cog.get_commands()
        for command in commands_:
            command_name = command.name
            command_aliases = command.aliases
            cmd = command_name
            if command_aliases:
                for alias in command_aliases:
                    cmd += f"|{alias}"
            command_description = f"![{cmd}]：{command.help}\n"
            manual += command_description
        manual += "-------\n"
    await ctx.send(manual)


class Pekobot(commands.Bot):
    """Representation of Pekobot.

    Attributes:
        session: A client session of aiohttp.
        g: A custom context dict.
    """
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop("command_prefix"))
        self.session = aiohttp.ClientSession(loop=self.loop)

        self.g = dict()  # inspired by flask.g
        self.g["pcr_db"] = kwargs.pop("pcr_db")

        self.remove_command("help")
        self.add_command(help_)
