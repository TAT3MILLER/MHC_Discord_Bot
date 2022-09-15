import asyncio
import discord
import os
import sqlite3
from bot import MHCBot
from decouple import config

bot = MHCBot()
discord.utils.setup_logging()

async def load_extensions():
    for name in os.listdir("./cogs"):
        if name.endswith(".py"):
            await bot.load_extension("cogs.{}".format(name[:-3]))


async def main():
    conn = sqlite3.connect('MHC.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS absolute_garbage (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quote TEXT,
        defense TEXT,
        datetime timestamp
        )""")
        
    c.execute("""CREATE TABLE IF NOT EXISTS hall_of_fame (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quote TEXT,
        datetime timestamp
        )""")
    conn.commit()
    conn.close()

    token = config("TOKEN")
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())