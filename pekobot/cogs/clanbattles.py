"""Clan battles cog"""
import datetime
import logging
import os
import shelve
import sqlite3

import discord
from discord.ext import commands

from pekobot.bot import Pekobot
from pekobot.utils import db

logger = logging.getLogger(__name__)

META_FILE_PATH = "clanbattles-meta.db"

CLAN_MEMBER_TABLE = "clan_member"
DELETE_MEMBER_FROM_CLAN = f'''
DELETE FROM {CLAN_MEMBER_TABLE}
WHERE member_id=%d;
'''

CLAN_BATTLE_TABLE = "clan_battle"
CREATE_CLAN_BATTLE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {CLAN_BATTLE_TABLE} (
    date TEXT PRIMARY KEY,
    name TEXt
)
"""
CREATE_NEW_CLAN_BATTLE = f"""
INSERT INTO {CLAN_BATTLE_TABLE} (date, name)
VALUES ('%s', '%s');
"""
COUNT_CLAN_BATTLE = f"""
SELECT COUNT(*) from {CLAN_BATTLE_TABLE}
WHERE date='%s';
"""
GET_CLAN_BATTLE_BY_DATE = f"""
SELECT date, name FROM {CLAN_BATTLE_TABLE}
WHERE date='%s'
"""


class ClanBattles(commands.Cog, name="公会战插件"):
    """The clan battles cog.

    Attributes:
        bot: A pekobot instance.
    """
    def __init__(self, bot: Pekobot):
        self.bot = bot

    @commands.command(name="create-clan", aliases=("建会", ))
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def create_clan(self, ctx: commands.Context):
        """创建公会。"""

        logger.info("Creating a clan for the guild %s.", ctx.guild)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            if not db.table_exists(conn, CLAN_MEMBER_TABLE):
                cursor = conn.cursor()
                create_table = f'''
                CREATE TABLE {CLAN_MEMBER_TABLE} (
                    member_id INTEGER PRIMARY KEY,
                    member_name TEXT,
                    member_nick TEXT
                )
                '''
                cursor.execute(create_table)
                logger.info("The clan %s has been created.", ctx.guild)
                await ctx.send("建会成功")
            else:
                logger.warning("The clan %s already exists.", ctx.guild)
                await ctx.send("公会已存在")

    @commands.command(name="join-clan", aliases=("入会", ))
    @commands.guild_only()
    async def join_clan(self, ctx: commands.Context):
        """加入公会。"""

        logger.info("%s (%s) is joining the clan.", ctx.author, ctx.guild)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            if not db.table_exists(conn, CLAN_MEMBER_TABLE):
                logger.error("The clan %s has not been created yet.",
                             ctx.guild)
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
                    logger.warning("%s is already in the clan %s.", author,
                                   ctx.guild)
                    await ctx.send("你已是公会成员")
                    return

                if author.nick:
                    nick = author.nick
                else:
                    nick = ""

                add_member = f'''
                INSERT INTO clan_member (member_id, member_name, member_nick)
                VALUES ({author.id}, '{author}', '{nick}');
                '''
                logger.info(
                    "Inserting (member_id: %d, member_name: '%s') into %s.",
                    author.id, author, CLAN_MEMBER_TABLE)
                cursor.execute(add_member)
                conn.commit()
                logger.info("%s has joined the clan %s.", author, ctx.guild)
                await ctx.send("入会成功")

    @commands.command(name="leave-clan", aliases=("退会", ))
    @commands.guild_only()
    async def leave_clan(self, ctx: commands.Context):
        """退出公会。"""

        logger.info("%s (%s) is leaving the clan.", ctx.author, ctx.guild)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            if not db.table_exists(conn, CLAN_MEMBER_TABLE):
                logger.error("The clan %s has not been created yet.",
                             ctx.guild)
                await ctx.send("公会尚未建立")
            else:
                cursor = conn.cursor()
                author = ctx.author
                check_member = f'''
                       SELECT COUNT(*) FROM clan_member
                       WHERE member_id={author.id};
                       '''
                cursor.execute(check_member)
                if cursor.fetchone()[0] == 0:
                    logger.warning("%s is not in the clan %s.", author,
                                   ctx.guild)
                    await ctx.send("你还不是公会成员")
                    return
                cursor.execute(DELETE_MEMBER_FROM_CLAN % author.id)
                conn.commit()
                logger.info("%s has left the clan %s.", author, ctx.guild)
                await ctx.send("退会成功")

    @commands.command(name="list-members", aliases=("查看成员", ))
    @commands.guild_only()
    async def list_members(self, ctx: commands.Context):
        """查看公会成员。"""

        logger.info("%s (%s) wants to list all members of the clan.",
                    ctx.author, ctx.guild)
        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            cursor = conn.cursor()
            if not db.table_exists(conn, CLAN_MEMBER_TABLE):
                logger.error("The clan %s has not been created yet.",
                             ctx.guild)
                await ctx.send("公会尚未建立")
            else:
                list_members = '''
                SELECT member_name, member_nick FROM clan_member;
                '''
                cursor.execute(list_members)
                display_names = []
                for name, nick in cursor.fetchall():
                    if not nick:
                        display_names.append(name)
                    else:
                        display_names.append(nick)
                if not display_names:
                    await ctx.send("暂无成员入会")
                    return
                report = '\n'.join(display_names)
                await ctx.send(report)

    @commands.command(name="start-clan-battle", aliases=("开始会战", ))
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def start_clan_battle(self, ctx: commands.Context, date="", name=""):
        """开始会战"""

        logger.info("%s (%s) is creating a new clan battle.", ctx.author,
                    ctx.guild)

        # validation on date
        if not date:
            logger.error("Empty date.")
            await ctx.send("请输入公会战日期")
            return
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            logger.error("Invalid date: %s", date)
            await ctx.send("请输入合法日期（YYYY-MM-DD）")
            return

        with sqlite3.connect(self._get_db_name(ctx)) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_CLAN_BATTLE_TABLE)

            cursor.execute(COUNT_CLAN_BATTLE % date)
            if cursor.fetchone()[0] != 0:
                logger.warning("Clan battle with date=%s already exists.",
                               date)
                await ctx.send("公会战已存在")
                return

            logger.info("Creating a new clan battle with date=%s and name=%s.",
                        date, name)
            cursor.execute(CREATE_NEW_CLAN_BATTLE % (date, name))
            await ctx.send("成功创建公会战")

            # Set this clan battle as the current clan battle.
            with shelve.open(META_FILE_PATH, writeback=True) as s:
                guid_id = str(ctx.guild.id)
                s[guid_id] = {
                    "current_battle_date": date,
                    "current_battle_name": name
                }
                logger.info("Current clan battle has been updated.")

    @commands.command(name="current-clan-battle", aliases=("当前会战", ))
    @commands.guild_only()
    async def show_current_clan_battle(self, ctx: commands.Context):
        """显示目前进行中公会战。"""

        logger.info("%s (%s) is requesting the current clan battle.",
                    ctx.author, ctx.guild)
        with shelve.open(META_FILE_PATH) as s:
            guild_id = str(ctx.guild.id)
            try:
                date = s[guild_id]["current_battle_date"]
                name = s[guild_id]["current_battle_name"]
                if name:
                    logger.info("Current clan battle: %s (%s)", date, name)
                    await ctx.send(f"当前公会战：{date} ({name})")
                else:
                    logger.info("Current clan battle: %s", date)
                    await ctx.send(f"当前公会战：{date}")
            except KeyError:
                logger.warning("Current clan battle does not exists.")
                await ctx.send("目前无进行中的公会战")

    @commands.command(name="export-data", aliases=("导出数据", ))
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def export_data(self, ctx: commands.Context):
        """导出公会战数据。"""

        id_ = ctx.author.id
        user = self.bot.get_user(id_)

        db_file = self._get_db_name(ctx)
        if os.path.exists(db_file):
            await user.send(file=discord.File(self._get_db_name(ctx)))
        else:
            await user.send("数据不存在")

    @staticmethod
    def _get_db_name(ctx: commands.Context) -> str:
        """Generates the DB name for a given guild.

        Args:
            ctx: A command context

        Returns:
            A table name.
        """

        guild_id = ctx.guild.id
        return f"clanbattles-{guild_id}.db"

    @staticmethod
    def _get_current_clan_battle(ctx: commands.Context) -> str:
        """Gets the current clan battle from the meta file.

        Args:
            ctx: A command context.

        Returns:
            The date of the current clan battle.
        """

        guild_id = str(ctx.guild.id)
        with shelve.open(META_FILE_PATH) as s:
            try:
                return s[guild_id]["current_battle"]
            except KeyError:
                return ""


def setup(bot):
    """A helper function used to load the cog."""

    bot.add_cog(ClanBattles(bot))