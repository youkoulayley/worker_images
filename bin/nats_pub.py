import asyncio
import json
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN


async def run(loop):
    nc = NATS()
    await nc.connect(io_loop=loop)

    sc = STAN()
    await sc.connect("serieall", "worker-images-sub", nats=nc)

    message = json.dumps({"url": "https://www.thetvdb.com/banners/fanart/original/5b0fcf2c5c1b5.jpg",
                          "name": "supergirl", "crop_type": "poster", "crop": "middle"}).encode()
    message2 = json.dumps({"url": "https://www.thetvdb.com/banners/graphical/295759-g2.jpg",
                          "name": "supergirl_banner", "crop_type": "banner", "crop": "middle"}).encode()
    await sc.publish("worker_images", message)
    await sc.publish("worker_images", message2)

    await sc.close()
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
