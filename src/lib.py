from typing import List, TypedDict, Union
from urllib import parse
from var import API_URL, BOT_ID, BOT_SECRET, CC, LL, LogLevel, TOKEN, LCL
from dotenv import load_dotenv
from disnake.ext import commands
from datetime import datetime
import aiohttp
import disnake
import json
import os

load_dotenv()
LOG_LEVEL = int(os.getenv("LOG_LEVEL", 3))
IF_LOG_WHITE_LIST = bool(os.getenv("IF_LOG_WHITE_LIST", False))
LOG_WHITE_LIST = json.dumps(os.getenv("LOG_WHITE_LIST", []))
LOG_BLACK_LIST = json.dumps(os.getenv("LOG_BLACK_LIST", []))


def urlencode(url) -> str:
    return parse.quote(str(url), safe="")


def color_text(text: str, color: CC) -> str:
    return f"{color.value}{text}{CC.RESET.value}"


def format_text(text: str, formats: List[CC]):
    return f"{''.join(map(lambda format: format.value, formats))}{text}{CC.RESET.value}" if formats else text


def bold_text(text: str) -> str:
    return f"{CC.BOLD.value}{text}{CC.RESET.value}"


class FMTOut:
    def color(text: str, color: CC, *, reset = True):
        return "{}{}{}".format(
            color.value,
            text,
            CC.RESET.value if reset else ""
        )

    def label(text: str, label: str):
        text_splitted = text.splitlines(keepends=True)
        return "".join(map(lambda text_piece: "{}{}".format(label, text_piece), text_splitted))

class Logger:
    level: LogLevel

    def __init__(self, level: LogLevel | int = LOG_LEVEL):
        self.level = LL(level)

    def log(self, msg: str, level: LogLevel | int = None, category: str = "others", custom_formats: list[CC] = []):
        if level == None:
            level = LL(self.level)
        else:
            level = LL(level)
        if level.value > self.level.value:
            return
        for cf in custom_formats:
            msg = FMTOut.color(msg, cf)
        label = "{:17} [{}] [{:12}]: ".format(datetime.now().strftime("%y-%m-%d %H:%M:%S"), level.name[:3], category)
        text = FMTOut.color(FMTOut.label(str(msg), label), LCL[level.name].value)
        print(text)

    def fatal(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 1, category, custom_formats = custom_formats)

    def error(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 2, category, custom_formats = custom_formats)

    def warn(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 3, category, custom_formats = custom_formats)

    def warning(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 3, category, custom_formats = custom_formats)

    def info(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 4, category, custom_formats = custom_formats)

    def debug(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 5, category, custom_formats = custom_formats)

    def trace(self, msg: str, category: str = "others", custom_formats: list[CC] = []):
        self.log(msg, 6, category, custom_formats = custom_formats)


def log_format(log_level: LL):
    return f"[ {log_level.name:7} ]"


def get_oauth_url(client_id: int | str, redirect_url: str, scope: List[str] = ["identify"], state=None) -> str:
    return f"{API_URL}/oauth2/authorize?client_id={urlencode(client_id)}&redirect_uri={urlencode(redirect_url)}&response_type=code&scope={urlencode('%20'.join(scope))}" + ("&state=" + urlencode(state)) if state else ""


class Commands(TypedDict):
    slash_commands: List[Union[disnake.APIUserCommand,
                               disnake.APIMessageCommand, disnake.APISlashCommand]]
    message_commands: List[commands.Command]


async def get_commands(bot: commands.Bot, *, message_commands=True, slash_commands=True, guild_id=None) -> Union[Commands, None]:
    if guild_id:
        return None
        # 後で実装
    else:
        result: Commands = dict()
        if slash_commands:
            result["slash_commands"] = await bot.fetch_global_commands()
        if message_commands:
            result["message_commands"] = bot.commands
        return result


class OAuth():
    token: str
    secret: str
    id: int
    session: aiohttp.ClientSession

    def __init__(self, *, token=None, secret=None, id=None):
        self.token = token or TOKEN
        self.secret = secret or BOT_SECRET
        self.id = id or BOT_ID

    def create_session(self) -> aiohttp.ClientSession:
        self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self) -> None:
        await self.session.close()
        del self.session

    async def post_form(self, url: str, headers: dict, data: dict):
        return await self.session.post(url, data=data, headers=headers)

    async def get_token(self, code: str):
        self.create_session()

