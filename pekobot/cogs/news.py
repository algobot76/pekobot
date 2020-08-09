"""News cog"""
import logging
from typing import List, Tuple

import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from pekobot.bot import Pekobot

logger = logging.getLogger(__name__)


async def fetch_news(
        session: aiohttp.ClientSession) -> List[Tuple[str, str, str]]:
    """Fetches news from https://priconne-redive.jp/news.

    Args:
        session: A client session of aiohttp.

    Returns:
        A list of articles.
    """

    async with session.get("https://priconne-redive.jp/news/") as resp:
        articles = []
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        for article in soup.find_all("div", class_="article_box"):
            link = article.find("a")["href"]
            title = article.find("h4").get_text()
            description_div = article.find("div", class_="description")
            description = description_div.find("p").get_text()
            articles.append((link, title, description))
        return articles


class News(commands.Cog, name="新闻插件"):
    """The news cog.

    Attributes:
        bot: A Pekobot instance.
    """
    def __init__(self, bot: Pekobot):
        self.bot = bot

    @commands.command(name="news", aliases=("新闻", ))
    async def get_news(self, ctx: commands.Context):
        """查看官方新闻。"""

        author = ctx.author
        logger.info("%s is requesting news.", author)
        articles = await fetch_news(self.bot.session)
        logger.info("Fetched %d articles.", len(articles))
        if not articles:
            await ctx.send("找不到官方新闻(｡╯︵╰｡)	")
            return
        description = self._get_description(articles)
        embed = discord.Embed(title="官方新闻", description=description)
        await ctx.send(embed=embed)

    @staticmethod
    def _get_description(articles: List[Tuple[str, str, str]]) -> str:
        result = '=======\n'
        for link, title, _ in articles:
            result += f"{title}\n"
            result += f"链接：{link}\n"
            result += "-------\n"
        return result


def setup(bot: Pekobot):
    """A helper function used to load the cog."""

    bot.add_cog(News(bot))
