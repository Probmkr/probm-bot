import json
from typing import List, TypedDict
from disnake.ext import commands
from lib import Logger
from var import DATABASE_URL, TOKEN, LL
from flask import Flask, request, jsonify
from webserver import web
import disnake

bot = commands.Bot(
    command_prefix="th!", intents=disnake.Intents.all(), reload=True
)
logger = Logger()
logger.log(f"log level is set to {logger.level.name}", LL.INFO)

bot.load_extension("cogs")

class State(TypedDict):
    guild: int
    role: int

@web.route("/verify")
async def verify():
    ip = None
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    code = request.args.get("code")
    state: State = json.loads(request.args.get("state"))
    logger.log(state, LL.DEBUG)
    role: disnake.Role = bot.get_guild(state["guild"]).get_role(state["role"])
    print(role)
    return jsonify({"code": code, "state": state, "ip": ip, "role": role.name})


bot.run(TOKEN)
