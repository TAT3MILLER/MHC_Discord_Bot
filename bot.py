import discord
from discord.ext import commands

class MHCBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(
            command_prefix = "!", 
            help_command = None,
            description = "MHC Bot", 
            intents = discord.Intents.all(), 
            **options)