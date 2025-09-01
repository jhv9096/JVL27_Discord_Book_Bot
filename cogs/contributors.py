# cogs/contributors.py

from discord.ext import commands
from db import insert_contributor, link_contributor_to_book, get_contributor_id_by_name, get_book_id_by_title
import psycopg2.errors

class Contributors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addcontributor(ctx, title: str, name: str, role: str):
        book_id = get_book_id_by_title(title)
        if not book_id:
            await ctx.send(f"❌ Book titled '{title}' not found in the database.")
            return

        contributor_id = get_contributor_id_by_name(name)
        if not contributor_id:
            contributor_id = insert_contributor(name)

        try:
            link_contributor_to_book(book_id, contributor_id, role)
            await ctx.send(f"✅ Contributor '{name}' added to *{title}* as [{role}].")
        except psycopg2.errors.UniqueViolation:
            await ctx.send(f"⚠️ Contributor '{name}' is already linked to *{title}* with role [{role}].")