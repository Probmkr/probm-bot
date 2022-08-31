from flask import Flask
from lib import Logger, LT

web: Flask = Flask(__name__)
logger = Logger()


def start_server() -> None:
    logger.log(LT.DEBUG, "starting server")
    web.run(port=3001)
