from discord.ext import commands

CREATE_CLAN_MEMBER_TABLE = '''
CREATE TABLE clan_member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
'''


class PCRClanBattles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_cursor = bot.db_conn.cursor()

    @commands.command(name="建会")
    @commands.guild_only()
    async def create_clan(self, ctx):
        self.db_cursor.execute(CREATE_CLAN_MEMBER_TABLE)
        await ctx.send("建会成功")


def setup(bot):
    bot.add_cog(PCRClanBattles(bot))
