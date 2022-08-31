from enum import Enum
import json
from typing import List, TypeAlias
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: str = os.getenv("BOT_TOKEN")
BOT_ID: int = int(os.getenv("BOT_ID"))
BOT_SECRET: str = os.getenv("BOT_SECRET")
ADMIN_IDS: List[int] = json.loads(os.getenv("ADMIN_IDS"))
ROLE_OAUTH_URL: str = os.getenv("ROLE_OAUTH_URL")
ROLE_OAUTH_SCOPE: List[str] = json.loads(os.getenv("ROLE_OAUTH_SCOPE", "[\"identify\"]"))

API_URL = "https://discord.com/api"
API_URL_V10 = "https://discord.com/api/v10"


class LogTypes(Enum):
    FATAL = 1
    ERROR = 2
    WARNING = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6


LT: TypeAlias = LogTypes
default_log_type: LT = LT(int(os.getenv("LOG_TYPE_NUM", "5")))
DLT: TypeAlias = default_log_type


class ConsoleColor(Enum):
    BLACK = '\033[30m'  # (文字)黒
    RED = '\033[31m'  # (文字)赤
    GREEN = '\033[32m'  # (文字)緑
    YELLOW = '\033[33m'  # (文字)黄
    BLUE = '\033[34m'  # (文字)青
    MAGENTA = '\033[35m'  # (文字)マゼンタ
    CYAN = '\033[36m'  # (文字)シアン
    WHITE = '\033[37m'  # (文字)白
    COLOR_DEFAULT = '\033[39m'  # 文字色をデフォルトに戻す
    BOLD = '\033[1m'  # 太字
    UNDERLINE = '\033[4m'  # 下線
    INVISIBLE = '\033[08m'  # 不可視
    REVERCE = '\033[07m'  # 文字色と背景色を反転
    BG_BLACK = '\033[40m'  # (背景)黒
    BG_RED = '\033[41m'  # (背景)赤
    BG_GREEN = '\033[42m'  # (背景)緑
    BG_YELLOW = '\033[43m'  # (背景)黄
    BG_BLUE = '\033[44m'  # (背景)青
    BG_MAGENTA = '\033[45m'  # (背景)マゼンタ
    BG_CYAN = '\033[46m'  # (背景)シアン
    BG_WHITE = '\033[47m'  # (背景)白
    BG_DEFAULT = '\033[49m'  # 背景色をデフォルトに戻す
    RESET = '\033[0m'  # 全てリセット


CC: TypeAlias = ConsoleColor


class LogColor(Enum):
    FATAL = CC.RED
    ERROR = CC.RED
    WARNING = CC.YELLOW
    INFO = CC.CYAN
    DEBUG = CC.GREEN
    TRACE = CC.WHITE


LC: TypeAlias = LogColor
