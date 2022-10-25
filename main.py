import discord
from discord import option
from utils import vt_file
import time
import os

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

DT_API_KEY = os.environ.get('DT_API_KEY')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for files to scan"))
    print(f"Connected as {bot.user}")


@bot.slash_command(name="ping", description="Pings the bot")
async def ping(ctx):
    embed=discord.Embed(color=0x333aff)
    embed.add_field(name="🏓 Pong! ", value=f"The bot latency is {round(bot.latency * 1000)}ms", inline=False)
    await ctx.respond(embed=embed)
    #await ctx.respond(f"🏓 Pong ({round(bot.latency * 1000)}ms)")


@bot.slash_command(name="check")
@option(
    "attachment",
    discord.Attachment,
    description="A mischievous attachment to scan...",
    # The default value will be None if the user doesn't provide a file.
    required=True,
)
async def say(
    ctx: discord.ApplicationContext,
    attachment: discord.Attachment,
):
    if attachment:
        await ctx.defer()
        file = await attachment.to_file()
        await attachment.save(file.filename)
        embed, img, f_name = vt_file(file.filename)
        os.remove(file.filename)
        await ctx.respond(embed=embed, file=img)
        os.remove(f_name)
    else:
        await ctx.respond("You didn't give me a file to reply with! :sob:")


bot.run(DT_API_KEY)
