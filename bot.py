# bot.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Run the bot
async def main():
    await load_cogs()
    await bot.start(os.getenv("DISCORD_TOKEN"))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Shutdown requested. BookBot shutting down.")