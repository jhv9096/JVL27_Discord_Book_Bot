from discord.ext import commands
from db.books import insert_book
from db.users import insert_user

bot = commands.Bot(command_prefix="!")

@bot.command()
async def addbook(ctx, title: str, source: str, format: str, genre: str):
    tags = ['example', 'demo']
    summary = 'Added via Discord bot.'
    url = None
    added_by = ctx.author.id

    # Track user
    insert_user(
        discord_id=ctx.author.id,
        username=ctx.author.name,
        discriminator=ctx.author.discriminator,
        nickname=ctx.author.nick
    )

    # Add book
    insert_book(title, source, format, genre, tags, summary, url, added_by)
    await ctx.send(f"✅ Book '{title}' added to the database!")