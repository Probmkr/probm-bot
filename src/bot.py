import json
from typing import List, TypedDict
from disnake.ext import commands
from db import DBC
from lib import Logger
from var import DATABASE_URL, TOKEN, LT
from flask import Flask, request, jsonify
from webserver import web
import disnake

bot = commands.Bot(
    command_prefix="th!", intents=disnake.Intents.all(), sync_commands=True, reload=True
)
logger = Logger()
db = DBC(DATABASE_URL)
logger.log(LT.INFO, f"log level is set to {logger.log_type.name}")

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
    logger.log(LT.DEBUG, state)
    role: disnake.Role = bot.get_guild(state["guild"]).get_role(state["role"])
    print(role)
    return jsonify({"code": code, "state": state, "ip": ip, "role": role.name})


bot.run(TOKEN)
