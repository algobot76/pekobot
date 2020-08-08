"""PCR clan battles cog"""
import logging
import sqlite3

from discord.ext import commands

from pekobot.pekobot import Pekobot
from pekobot.utils import db

logger = logging.getLogger(__name__)


class PCRClanBattles(commands.Cog, name="PCR公会战插件"):
    """The PCR clan battles cog.

    Attributes:
        bot: A pekobot instance.
    """

    CLAN_MEMBER_TABLE = "clan_member"

    def __init__(self, bot: Pekobot):
        self.bot = bot

    @commands.command(name="create-clan", aliases=("建会", ))
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def create_clan(self, ctx: commands.Context):
        """创建公会。"""

        logger.info("Creating a clan for the guild %s.", ctx.guild)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            if not db.table_exists(conn, self.CLAN_MEMBER_TABLE):
                cursor = conn.cursor()
                create_table = f'''
                CREATE TABLE {self.CLAN_MEMBER_TABLE} (
                    member_id INTEGER PRIMARY KEY,
                    member_name TEXT
                )
                '''
                cursor.execute(create_table)
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
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            if not db.table_exists(conn, self.CLAN_MEMBER_TABLE):
                logger.error("The clan has not been created yet.")
                await ctx.send("公会尚未建立")
            else:
                cursor = conn.cursor()
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
                    author.id, author, self.CLAN_MEMBER_TABLE)
                cursor.execute(add_member)
                conn.commit()
                logger.info("%s has joined the clan.", author)
                await ctx.send("入会成功")

    @commands.command(name="list-members", aliases=("查看成员", ))
    @commands.guild_only()
    async def list_members(self, ctx: commands.Context):
        """查看公会成员。"""

        logger.info("%s wants to list all members of the clan.", ctx.author)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            cursor = conn.cursor()
            if not db.table_exists(conn, self.CLAN_MEMBER_TABLE):
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

    @staticmethod
    def _get_db_name(ctx: commands.Context) -> str:
        """Generates the DB name for a given guild.

        Args:
            ctx: A command context
        """

        guid_id = ctx.guild.id
        return f"pcrclanbattles-{guid_id}.db"


def setup(bot):
    """A helper function used to load the cog."""

    bot.add_cog(PCRClanBattles(bot))
