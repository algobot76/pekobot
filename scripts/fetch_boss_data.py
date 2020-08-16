# pylint: skip-file
import asyncio
import json
import os

import aiohttp
import yaml

BOSS_DATA_URL = "https://raw.githubusercontent.com/Ice-Cirno/HoshinoBot/master/hoshino/modules/pcrclanbattle/clanbattle/config.json"
OUTPUT_PATH = os.path.join("data", "boss_data.yaml")


async def run():
    async with aiohttp.ClientSession() as session:
        async with session.get(BOSS_DATA_URL) as resp:
            if resp.status != 200:
                print("Failed to fetch the boss data!")
                return
            content = await resp.text()
            data = json.loads(content)
            for k in ["_comment_CN", "_comment_TW"]:
                if k in data:
                    del data[k]
            with open(OUTPUT_PATH, "w") as out:
                yaml.dump(data, out)


asyncio.run(run())
