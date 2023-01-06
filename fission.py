from func.main import update_politically_exposed_us
import asyncio

import uvloop
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from hypercorn.asyncio import serve
from hypercorn.config import Config

app = Flask(__name__)


@app.route('/specialize', methods=['POST'])
async def load():
    return ""


@app.route('/v2/specialize', methods=['POST'])
async def loadv2():
    return ""


@app.route('/healthz', methods=['GET'])
async def healthz():
    return "", 200


@app.route('/', methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE'])
async def f():
    return await update_politically_exposed_us()


asgi_app = WsgiToAsgi(app)

conf = Config()
conf.bind = f"0.0.0.0:8888"

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(serve(asgi_app, conf))
