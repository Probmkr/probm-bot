from enum import Enum
from typing import TypeAlias
from dotenv import load_dotenv
import os

load_dotenv()

class LogTypes(Enum):
    FATAL=1
    ERROR=2
    WARNING=3
    INFO=4
    DEBUG=5
    TRACE=6

LT: TypeAlias = LogTypes

default_log_type: LT = LT(int(os.getenv("LOG_TYPE_NUM", "5")))

DLT: TypeAlias = default_log_type

def log_format(log_type: LT):
    return f"[ {log_type.name:7} ]"

class Logger:
    def __init__(self, log_type: LogTypes):
        self.log_type = log_type

    def log(self, log_type: LogTypes, message: str):
        if log_type.value <= self.log_type.value:
            print(f"{log_format(log_type)}: {message}".replace("\n", f"\n{log_format(log_type)}: "))