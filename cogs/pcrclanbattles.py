from discord.ext import commands

from utils import db

DB_NAME = "pcrclanbattles.db"

CLAN_MEMBER_TABLE = "clan_member"

CREATE_CLAN_MEMBER_TABLE = f'''
CREATE TABLE {CLAN_MEMBER_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
'''


class PCRClanBattles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pcb_db = db.create_connection(DB_NAME)  # PCB = PCR Clan Battles

    @commands.command(name="建会")
    @commands.guild_only()
    async def create_clan(self, ctx):
        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            cursor = self.pcb_db.cursor()
            cursor.execute(CREATE_CLAN_MEMBER_TABLE)
            await ctx.send("建会成功")
        else:
            await ctx.send("公会已存在")


def setup(bot):
    bot.add_cog(PCRClanBattles(bot))
