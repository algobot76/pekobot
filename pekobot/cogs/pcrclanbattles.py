"""PCR clan battles cog"""
import logging

from discord.ext import commands

from pekobot.bot import Bot
from pekobot.utils import db

logger = logging.getLogger(__name__)

DB_NAME = "pcrclanbattles.db"

CLAN_MEMBER_TABLE = "clan_member"

CREATE_CLAN_MEMBER_TABLE = f'''
CREATE TABLE {CLAN_MEMBER_TABLE} (
    member_id INTEGER PRIMARY KEY,
    member_name TEXT
)
'''


class PCRClanBattles(commands.Cog, name="PCR公会战插件"):
    """The PCR clan battles cog.

    Attributes:
        bot: A pekobot instance.
        pcb_cb: A DB connection to PCB.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.pcb_db = db.create_connection(DB_NAME)  # PCB = PCR Clan Battles

    @commands.command(name="create-clan", aliases=("建会", ))
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def create_clan(self, ctx: commands.Context):
        """创建公会。"""

        logger.info("Creating a clan for the guild %s.", ctx.guild)
        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            cursor = self.pcb_db.cursor()
            cursor.execute(CREATE_CLAN_MEMBER_TABLE)
            logger.info("The clan has been created.")
            await ctx.send("建会成功")
        else:
            logger.warning("The clan already exists.")
            await ctx.send("公会已存在")

    @commands.command(name="join-clan", aliases=("入会", ))
    @commands.guild_only()
    async def join_clan(self, ctx: commands.Context):
        """加入公会。"""

        logger.info("%s is trying to join the clan.", ctx.author)

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
                logger.warning("%s is already in the clan.", author)
                await ctx.send("你已是公会成员")
                return

            add_member = f'''
            INSERT INTO clan_member (member_id, member_name)
            VALUES ({author.id}, '{author}');
            '''
            logger.info(
                "Inserting (member_id: %d, member_name: '%s') into %s.",
                author.id, author, CLAN_MEMBER_TABLE)
            cursor.execute(add_member)
            self.pcb_db.commit()
            logger.info("%s has joined the clan.", author)
            await ctx.send("入会成功")

    @commands.command(name="list-members", aliases=("查看成员", ))
    @commands.guild_only()
    async def list_members(self, ctx: commands.Context):
        """查看公会成员。"""

        logger.info("%s wants to list all members of the clan.", ctx.author)

        cursor = self.pcb_db.cursor()
        if not db.table_exists(self.pcb_db, CLAN_MEMBER_TABLE):
            logger.error("The clan has not been created yet.")
            await ctx.send("公会尚未建立")
        else:
            list_members = '''
            SELECT member_name FROM clan_member;
            '''
            cursor.execute(list_members)
            names = [name for name, in cursor.fetchall()]
            if not names:
                await ctx.send("暂无成员入会")
                return
            report = '\n'.join(names)
            await ctx.send(report)


def setup(bot):
    """A helper function used to load the cog."""

    bot.add_cog(PCRClanBattles(bot))
