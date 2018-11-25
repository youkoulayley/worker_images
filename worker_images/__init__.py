import asyncio
from nats.aio.client import Client as NATS
from flask import Flask
from multiprocessing import Process, Value

app = Flask(__name__)
from worker_images import nats_client, router


def nats_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop))
    loop.close()


if __name__ == '__main__':
    recording_on = Value('b', True)
    p = Process(target=nats_loop, args=(recording_on,))
    p.start()
    app.run()
    p.join()
