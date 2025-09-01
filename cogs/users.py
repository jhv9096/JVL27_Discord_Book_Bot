# cogs/users.py

from discord.ext import commands

class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pinguser(self, ctx):
        await ctx.send(f"👤 You are {ctx.author.name}#{ctx.author.discriminator}")

async def setup(bot):
    await bot.add_cog(Users(bot))