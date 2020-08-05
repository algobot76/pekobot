from discord.ext import commands


def is_admin():
    async def predicate(ctx: commands.Context):
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        if not permissions.administrator:
            await ctx.send("此功能只对管理员开放")
            return False
        return True

    return commands.check(predicate)


def is_nsfw():
    async def predicate(ctx: commands.Context):
        ch = ctx.channel

        if not ch.is_nsfw():
            await ctx.send("你在想啥呢？变态ヽ(`⌒´メ)ノ")
            return False
        return True

    return commands.check(predicate)
