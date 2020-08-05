import logging

from bs4 import BeautifulSoup
from discord.ext import commands

from pekobot.bot import Bot

logger = logging.getLogger(__name__)


async def fetch_news(session):
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


class PCRNews(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="news", aliases=("新闻", ))
    async def get_news(self, ctx: commands.Context):
        author = ctx.author
        logger.info(f"{author} is requesting PCR news.")
        articles = await fetch_news(self.bot.session)
        logger.info(f"Fetched {len(articles)} articles.")
        if not articles:
            await ctx.send("找不到官方新闻(｡╯︵╰｡)	")
        for link, _, _ in articles:
            await ctx.send(link)


def setup(bot: Bot):
    bot.add_cog(PCRNews(bot))
