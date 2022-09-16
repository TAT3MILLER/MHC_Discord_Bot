from urllib import response
import discord
from discord.ext import commands
from discord import Embed
import sqlite3
import datetime

class Commands(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")

    
    @commands.command()
    async def ag(self, ctx):
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
        c.execute("INSERT INTO absolute_garbage(name, quote, defense, datetime) VALUES (?, ? , ?, ?)", data)

        try:
            conn.commit()
        except:
            await ctx.send("Could not commit to database")
        await ctx.send('Saved',delete_after = 5)
        conn.close()

    @commands.command()
    async def hof(self, ctx):
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
        c.execute("INSERT INTO hall_of_fame(name, quote, datetime) VALUES (?, ? , ?)", data)

        try:
            conn.commit()
        except:
            await ctx.send("Could not commit to database")
        await ctx.send('Saved',delete_after = 5)
        conn.close()

    @commands.command()
    async def aglist(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT * FROM absolute_garbage")
        rows = c.fetchall()
        for row in rows:
            entry = row[1] + ': "' + row[2] + '"  Defense: "' + row[3] + '"  Said on: ' + row[4] + "\n"
            await ctx.send(entry)
        conn.close()

    @commands.command()
    async def hoflist(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("Select * FROM hall_of_fame")
        rows = c.fetchall()

        for row in rows:
            entry = row[1] + ': "' + row[2] + '" ' + 'Said on: ' + row[3]
            await ctx.send(entry)
        conn.close()

    @commands.command()
    async def agdeletelast(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM absolute_garbage")
        row = c.fetchone()
        c.execute("DELETE FROM absolute_garbage WHERE id=?", row)
        try:
            conn.commit()
        except:
            await ctx.send("Could not delete from database")
        await ctx.send('Deleted',delete_after = 5)
        conn.close()

    @commands.command()
    async def hofdeletelast(self, ctx, description="Will delete the last "):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM hall_of_fame")
        row = c.fetchone()
        c.execute("DELETE FROM hall_of_fame WHERE id=?", row)
        try:
            conn.commit()
        except:
            await ctx.send("Could not delete from database")
        await ctx.send('Deleted',delete_after = 5)
        conn.close()

    @commands.command()
    async def agcount(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM absolute_garbage")
        row = str(c.fetchone())
        await ctx.send(row[1])
        conn.close()

    @commands.command()
    async def hofcount(self, ctx):
        conn = sqlite3.connect('MHC.db')
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM hall_of_fame")
        row = str(c.fetchone())
        await ctx.send(row[2])
        conn.close()


class HelpCog(commands.Cog, name = "Help"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self



class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='Commands \n')
        help_commands = {
            "!ag": "Add a quote to Absolute Garbage",
            "!aglist": "List all quotes from Absolute Garbage",
            "!agdeletelast": "Delete last entry into Absolute Garbage",
            "!agcount": "Lists number of entries in Absolute Garbage",
            "!hof": "Add a quote to Hall of Fame",
            "!hoflist": "List all quotes from Hall of Fame",
            "!hofdeletelast": "Delete last entry from Hall of Fame",
            "!hofcount": "Lists number of entries in Hall of Fame"
        }
        for key, value in help_commands.items():
            e.description += f'{key} -> {value} \n'
        
        
        await destination.send(embed=e)

async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.add_cog(HelpCog(bot))
    