from discord.ext import commands

from utils import config

conf = config.load_config()
bot = commands.Bot(command_prefix=("!", "！"))

for cog in conf["cogs"]:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="foo")
async def foo(ctx):
    await ctx.send("Bar")


@bot.command(name="sum")
async def _sum(ctx, *args):
    result = sum(map(int, args))
    await ctx.send(f'Sum: {result}')


bot.run(conf['discord_token'])
