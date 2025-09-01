# cogs/books.py

from discord.ext import commands

from db import insert_book, get_all_books, get_book_summaries

print("Books cog loaded")
class Books(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addbook(self, ctx, title: str, source: str, book_format: str, genre: str):
        tags = ['example', 'demo']
        summary = 'Added via Discord bot.'
        url = None
        added_by = ctx.author.id

        insert_book(title, source, book_format, genre, tags, summary, url, added_by)
        await ctx.send(f"✅ Book '{title}' added to the database!")

    @commands.command()
    async def listbooks(self, ctx):
        books = get_all_books()
        print("DEBUG: books =", books)
        if not books:
            await ctx.send("📚 No books found in the library.")
            return

        message = "**Books in the Library:**\n"
        for title, _, _ in books:
            message += f"• {title}\n"
        await ctx.send(message)

    @commands.command()
    async def listbooksplus(self, ctx):
        rows = get_book_summaries()
        if not rows:
            await ctx.send("📚 No books found in the library.")
            return

        from collections import defaultdict
        book_map = defaultdict(list)

        for book_id, title, book_format, source, has_contributors, role, contributor in rows:
            book_map[book_id].append((title, book_format, source, has_contributors, role, contributor))

        message = "**Books in the Library:**\n"
        for entries in book_map.values():
            title, book_format, source, has_contributors, _, _ = entries[0]
            contributor_lines = [
                f"{contributor} [{role}]" for _, _, _, _, role, contributor in entries if contributor
            ]
            contributor_display = ", ".join(contributor_lines) if contributor_lines else "⚠️ No contributors listed"
            message += f"• *{title}* ({book_format}) — Source: {source}\n   Contributors: {contributor_display}\n\n"

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Books(bot))