import logging

from discord.ext import commands

from pekobot.utils import checks, db

logger = logging.getLogger(__name__)

DB_NAME = "pcrclanbattles.db"

CLAN_MEMBER_TABLE = "clan_member"

CREATE_CLAN_MEMBER_TABLE = f'''
CREATE TABLE {CLAN_MEMBER_TABLE} (
    member_id INTEGER PRIMARY KEY,
    member_name TEXT
)
'''


class PCRClanBattles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pcb_db = db.create_connection(DB_NAME)  # PCB = PCR Clan Battles

    @commands.command(name="建会")
    @commands.guild_only()
    @checks.is_admin()
    async def create_clan(self, ctx: commands.Context):
        logger.info(f"Creating a clan for the guild {ctx.guild}.")
        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            cursor = self.pcb_db.cursor()
            cursor.execute(CREATE_CLAN_MEMBER_TABLE)
            logger.info("The clan has been created.")
            await ctx.send("建会成功")
        else:
            logger.warning("The clan already exists.")
            await ctx.send("公会已存在")

    @commands.command(name="入会")
    @commands.guild_only()
    async def join_clan(self, ctx: commands.Context):
        logger.info(f"{ctx.author} is trying to join the clan.")

        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            logger.error("The clan has not been created yet.")
            await ctx.send("公会尚未建立")
        else:
            cursor = self.pcb_db.cursor()
            author = ctx.author
            check_member = f'''
            SELECT COUNT(*) FROM clan_member
            WHERE member_id={author.id};
            '''
            cursor.execute(check_member)
            if cursor.fetchone()[0] != 0:
                logger.warning(f"{author} is already in the clan.")
                await ctx.send("你已是公会成员")
                return

            add_member = f'''
            INSERT INTO clan_member (member_id, member_name)
            VALUES ({author.id}, '{author}');
            '''
            logger.info(
                f"Inserting (member_id: {author.id}, member_name: '{author}') into {CLAN_MEMBER_TABLE}."
            )
            cursor.execute(add_member)
            self.pcb_db.commit()
            logger.info(f"{author} has joined the clan.")
            await ctx.send("入会成功")


def setup(bot):
    bot.add_cog(PCRClanBattles(bot))
