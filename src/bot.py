from disnake.ext import commands
from lib import Logger
from cogs import *
from var import TOKEN
import disnake

bot = commands.Bot(command_prefix='th!',
                   intents=disnake.Intents.all(), sync_commands=True, reload=True)
logger = Logger()
logger.log(LT.INFO, f"log level is set to {logger.log_type.name}")

bot.add_cog(Ping(bot))
bot.add_cog(MessagePing(bot))
bot.add_cog(Verify(bot))
bot.add_cog(OnReady(bot))
bot.add_cog(LogCommands(bot))

# @bot.command()
# async def ping(ctx: commands.Context):
#     await ctx.send("pong!")

bot.run(TOKEN)
