import logging

import discord
from discord.ext import commands

from utils import db

logger = logging.getLogger(__name__)

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
    async def create_clan(self, ctx: discord.ext.commands.Context):
        logger.info(f"Creating a clan for the guild {ctx.guild}.")
        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            cursor = self.pcb_db.cursor()
            cursor.execute(CREATE_CLAN_MEMBER_TABLE)
            logger.info("The clan has been created.")
            await ctx.send("建会成功")
        else:
            logger.warning("The clan already exists.")
            await ctx.send("公会已存在")


def setup(bot):
    bot.add_cog(PCRClanBattles(bot))
