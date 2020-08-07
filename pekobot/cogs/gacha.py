"""Gacha cog"""
import asyncio
import io
import random

import discord
from PIL import Image
from discord.ext import commands


def get_unit_icon_id(unit_id, rarity):
    """Generates a unit icon ID.

    Args:
        unit_id: ID of a unit.
        rarity: Rarirty of a unit (1-3).

    Returns:
        IF of a unit icon.
    """
    return int(unit_id) + rarity * 10


async def download_unit_icon(session, unit_icon_id):
    """Downloads an icon.

    Args:
        session: A client session of aiohttp.
        unit_icon_id: ID of a unit icon.

    Returns:
        A tuple that contains the ID of a unit icon and its data in bytes.
    """
    url = f"https://redive.estertion.win/icon/unit/{unit_icon_id}.webp"
    async with session.get(url) as resp:
        data = io.BytesIO(await resp.read())
        return unit_icon_id, data


def combine_images_h(images):
    """Combines images horizontally.

    Args:
        images: A list of images.

    Returns:
        A single image.
    """
    sample_image = images[0]
    result = Image.new("RGB",
                       (sample_image.width * len(images), sample_image.height))
    for i, image in enumerate(images):
        result.paste(image, (sample_image.width * i, 0))
    return result


def bytes_to_image(buf):
    """Converts bytes to an image.

    Args:
        buf: Image data in bytes.

    Returns:
        An image.
    """
    return Image.open(buf)


def image_to_bytes(image):
    """Converts an image to its data in bytes.

    Args:
        image: An image

    Returns:
        Image data in  bytes.
    """
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf


class Gacha(commands.Cog, name="抽卡插件"):
    """Gacha cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gacha", aliases=("抽卡", "扭蛋"))
    async def rolls(self, ctx, n="10"):
        """模拟抽卡（默认：10连）。"""

        # n must be a number
        if not n.isdigit():
            await ctx.send("草，别输入一些乱七八糟的东西啊！！！")
            return

        n = int(n)

        # n must be >= 1 and <=10
        if n < 1 or n > 10:
            await ctx.send("请输入1和10之间的数字")
            return
        conn = self.bot.g.get("pcr_db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT unit_id, rarity, is_limited, comment
        FROM unit_data
        ''')

        characters = dict()
        for row in cursor.fetchall():
            unit_id, rarity, is_limited, comment = row
            if rarity == 2:
                rarity -= 1
            if comment:
                characters[str(unit_id)] = (rarity, is_limited)

        items = list(characters.items())

        # only keep non-limited characters
        items = [item for item in items if item[1][1] == 0]

        # TODO: Allow duplicate characters
        selected = random.choices(items, k=n)
        download_requests = []
        # TODO: Cache image files
        for item in selected:
            unit_id = item[0]
            rarity = item[1][0]
            unit_icon_id = get_unit_icon_id(unit_id, rarity)
            download_requests.append(
                download_unit_icon(self.bot.session, unit_icon_id))
        downloaded_images = await asyncio.gather(*download_requests)
        images = [bytes_to_image(image[1]) for image in downloaded_images]
        gacha_result = image_to_bytes(combine_images_h(images))
        await ctx.send("素敵な仲間が増えますよ！")
        await ctx.send(file=discord.File(gacha_result, "gacha_result.png"))


def setup(bot):
    """A helper function used to load the cog."""

    bot.add_cog(Gacha(bot))
