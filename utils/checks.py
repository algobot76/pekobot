import discord.ext
from discord.ext import commands


def is_admin():
    async def predicate(ctx: discord.ext.commands.Context):
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        if not permissions.administrator:
            await ctx.send("此功能只对管理员开放")
            return False
        return True

    return commands.check(predicate)
