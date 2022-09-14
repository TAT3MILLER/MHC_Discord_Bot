from urllib import response
import discord
from discord.ext import commands
import sqlite3
import datetime

class Commands(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")


    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello")

    @commands.command()
    async def AG(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()

        def check(m):
            return m.author.id == ctx.author.id

        await ctx.send('Offender?')
        offender = await self.bot.wait_for('message', check = check)

        await ctx.send('Quote?')
        quote = await self.bot.wait_for('message', check = check)

        await ctx.send('Defense?')
        defense = await self.bot.wait_for('message', check = check)

        now = datetime.datetime.now()
        date = now.strftime("%m/%d/%Y  %H:%M:%S")
        data = (offender.content, quote.content, defense.content, date)
        c.execute("INSERT INTO absolute_garbage VALUES (?, ? , ?, ?)", data)

        try:
            conn.commit()
        except:
            await ctx.send("Could not commit to database")
        await ctx.send('Saved')
        conn.close()

    @commands.command()
    async def HOF(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()

        def check(m):
            return m.author.id == ctx.author.id

        await ctx.send('Fella who be talking they shit?')
        name = await self.bot.wait_for('message', check=check)

        await ctx.send('Quote?')
        quote = await self.bot.wait_for('message', check=check)

        now = datetime.datetime.now()
        date = now.strftime("%m/%d/%Y  %H:%M:%S")
        data = (name.content, quote.content, date)
        c.execute("INSERT INTO hall_of_fame VALUES (?, ? , ?)", data)

        try:
            conn.commit()
        except:
            await ctx.send("Could not commit to database")
        await ctx.send('Saved')
        conn.close()

    @commands.command()
    async def ag_list(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT * FROM absolute_garbage")
        rows = c.fetchall()

        for row in rows:
            message = str(row)
            await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Commands(bot))