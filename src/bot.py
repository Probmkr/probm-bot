from disnake.ext import commands
from lib import Logger
from cogs import *
from var import TOKEN
from flask import Flask, request, jsonify
import disnake

bot = commands.Bot(command_prefix='th!',
                   intents=disnake.Intents.all(), sync_commands=True, reload=True)
logger = Logger()
logger.log(LT.INFO, f"log level is set to {logger.log_type.name}")

# @bot.command()
# async def ping(ctx: commands.Context):
#     await ctx.send("pong!")

bot.load_extension('cogs')

bot.run(TOKEN)
