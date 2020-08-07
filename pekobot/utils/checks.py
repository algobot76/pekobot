"""A decorator module build on top of discord.ext.commands.check.
This module contains various decorators used to validate discord commands. For
example, you can use is_admin() to make sure the command can only be called by
an administrator.
"""
from discord.ext import commands


def is_admin():
    """Checks if the user is an administrator."""
    async def predicate(ctx: commands.Context) -> bool:
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        if not permissions.administrator:
            await ctx.send("此功能只对管理员开放")
            return False
        return True

    return commands.check(predicate)


def is_nsfw():
    """Checks if the channel is a NSFW channel."""
    async def predicate(ctx: commands.Context) -> bool:
        ch = ctx.channel

        if not ch.is_nsfw():
            await ctx.send("你在想啥呢？变态ヽ(`⌒´メ)ノ")
            return False
        return True

    return commands.check(predicate)
