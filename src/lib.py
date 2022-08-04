from typing import List
from urllib import parse
from var import API_URL, CC, LC, LT, DLT
from dotenv import load_dotenv

load_dotenv()


def urlencode(url):
    return parse.quote(url, safe="")


def color_text(text: str, color: CC):
    return f"{color.value}{text}{color.value}{CC.COLOR_DEFAULT.value}"


class Logger:
    def __init__(self, log_type: LT = DLT):
        self.log_type = log_type

    def log(self, log_type: LT, message: str):
        if log_type.value <= self.log_type.value:
            print_text = color_text(f"{log_format(log_type)}: {message}"
                                    .replace("\n", f"\n{log_format(log_type)}: "), LC[log_type.name].value)
            print(print_text)


def log_format(log_type: LT):
    return f"[ {log_type.name:7} ]"


def get_oauth_url(client_id: int | str, redirect_url: str, scope: List[str] = ["identify"], state=None):
    return f"{API_URL}/oauth2/authorize?client_id={client_id}&redirect_uri={urlencode(redirect_url)}&response_type=code&scope={'%20'.join(scope)}" + ("&state=" + urlencode(state)) if state else ""
