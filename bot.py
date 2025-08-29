import os

import discord
from discord.ext import commands
from db import insert_book, insert_user, insert_contributor, link_contributor_to_book, get_book_summaries, get_all_books
from collections import defaultdict

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
    books = get_all_books()  # Returns list of (title, format, source)
    if not books:
        await ctx.send("📚 No books found in the library.")
        return

    message = "**Books in the Library:**\n"
    for title, _, _ in books:  # Unpack the tuple, ignore format and source
        message += f"• {title}\n"
    await ctx.send(message)

@bot.command()
async def listbook_summaries(ctx):
    rows = get_book_summaries()  # Returns list of tuples from the query above

    if not rows:
        await ctx.send("📚 No books found in the library.")
        return

    book_map = defaultdict(list)

    for book_id, title, book_format, source, has_contributors, contributor, role in rows:
        book_map[book_id].append((title, book_format, source, has_contributors, contributor, role))

    message = "**Book Summaries:**\n"
    for entries in book_map.values():
        title, book_format, source, has_contributors, _, _ = entries[0]
        contributor_lines = []

        for _, _, _, _, contributor, role in entries:
            if contributor:
                contributor_lines.append(f"{contributor} [{role}]")

        contributor_display = ", ".join(contributor_lines) if contributor_lines else "⚠️ No contributors listed"

        message += f"• *{title}* ({book_format}) — Source: {source}\n   Contributors: {contributor_display}\n\n"

    await ctx.send(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(os.getenv("DISCORD_TOKEN"))