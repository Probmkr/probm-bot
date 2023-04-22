import os
from flask import Flask
from lib import Logger, LL
from wsgiref import simple_server
from dotenv import load_dotenv

load_dotenv
PORT = os.getenv("PORT", 3000)
web: Flask = Flask(__name__)
logger = Logger()


def start_server() -> None:
    class CustomLogServer(simple_server.WSGIRequestHandler):
        def log_message(self, format, *args):
            logger.debug("{} > {}".format(
                self.client_address[0], format % args), "web")
    server = simple_server.make_server(
        '0.0.0.0', PORT, web, handler_class=CustomLogServer)
    logger.info(f"{PORT}番ポートでWebページの起動に成功しました", "web")
    server.serve_forever()
