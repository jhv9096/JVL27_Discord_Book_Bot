import os

import discord
from discord.ext import commands
from db import insert_book, insert_user, insert_contributor, link_contributor_to_book, get_book_summaries

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def addbook(ctx, title: str, source: str, book_format: str, genre: str):
    tags = ['example', 'demo']
    summary = 'Added via Discord bot.'
    url = None
    added_by = ctx.author.id

    # Track user
    insert_user(
        discord_id=ctx.author.id,
        username=ctx.author.name,
        discriminator=ctx.author.discriminator,
        nickname = ctx.author.nick if ctx.author.nick else ctx.author.name
    )

    # Add book
    insert_book(title, source, book_format, genre, tags, summary, url, added_by)
    await ctx.send(f"✅ Book '{title}' added to the database!")

@bot.command()
async def listbooks(ctx):
    books = get_book_summaries()
    if not books:
        await ctx.send("📚 No books found in the database.")
        return

    message = "**Books in the Library:**\n"
    for title, book_format, source, url, role, contributor in books:
        line = f"• *{title}* ({format}) by {contributor} [{role}]"
        if source:
            line += f" — Source: {source}"
        if url:
            line += f" — [Link]({url})"
        message += line + "\n"

    await ctx.send(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(os.getenv("DISCORD_TOKEN"))