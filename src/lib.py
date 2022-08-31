from typing import List, TypedDict, Union
from urllib import parse
from var import API_URL, BOT_ID, BOT_SECRET, CC, LC, LT, DLT, ROLE_OAUTH_SCOPE, ROLE_OAUTH_URL, TOKEN
from dotenv import load_dotenv
from disnake.ext import commands
import aiohttp
import asyncio
import disnake

load_dotenv()


def urlencode(url) -> str:
    return parse.quote(str(url), safe="")


def color_text(text: str, color: CC) -> str:
    return f"{color.value}{text}{CC.RESET.value}"


def format_text(text: str, formats: List[CC]):
    return f"{''.join(map(lambda format: format.value, formats))}{text}{CC.RESET.value}" if formats else text


def bold_text(text: str) -> str:
    return f"{CC.BOLD.value}{text}{CC.RESET.value}"


class Logger:
    def __init__(self, log_type: LT = DLT):
        self.log_type = log_type

    def log(self, log_type: LT, message: str, *, custom_formats: List[CC] = None) -> None:
        if log_type.value <= self.log_type.value:
            print_text = format_text(
                color_text(
                    f"{log_format(log_type)}: {message}".replace(
                        "\n", f"\n{log_format(log_type)}: "),
                    LC[log_type.name].value
                ), custom_formats
            )
            print(print_text)


def log_format(log_type: LT):
    return f"[ {log_type.name:7} ]"


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

