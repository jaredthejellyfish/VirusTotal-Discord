import discord
from discord import option
from utils import vt_file, format_resp_data
import time
import os

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

DT_API_KEY = os.environ.get('DT_API_KEY')

@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")


@bot.slash_command(name="ping")
async def ping(ctx):
    await ctx.respond(f"🏓 Pong ({round(bot.latency * 1000)}ms)")


@bot.slash_command(name="check")
@option(
    "attachment",
    discord.Attachment,
    description="A file to attach to the message",
    # The default value will be None if the user doesn't provide a file.
    required=False,
)
async def say(
    ctx: discord.ApplicationContext,
    attachment: discord.Attachment,
):
    if attachment:
        await ctx.defer()
        file = await attachment.to_file()
        await attachment.save(file.filename)
        embed, file = vt_file(file.filename)
        os.remove(file.filename)
        
        await ctx.respond(embed=embed, file=file)
    else:
        await ctx.respond("You didn't give me a file to reply with! :sob:")

bot.run(DT_API_KEY)
