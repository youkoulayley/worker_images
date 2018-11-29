import logging
import os
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
logger = logging.getLogger("worker_images")
cluster_id = config.get_config('NATS', 'cluster_id')
channel = config.get_config('NATS', 'channel')
client_id = str(os.getpid())


async def run(loop):
    nc = NATS()
    sc = STAN()

    # Start session with NATS Streaming cluster using the established NATS connection.
    await nc.connect(io_loop=loop)

    logger.debug("Connecting to NATS streaming server")
    await sc.connect(cluster_id=cluster_id, client_id=application_name, nats=nc)
    logger.info("Connected to NATS streaming server")

    # Example async subscriber
    async def cb(msg):
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe(channel, durable_name=application_name, start_at="first", cb=cb)
