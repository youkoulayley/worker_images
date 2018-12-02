import logging
import json
import os
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
from worker_images import config, worker

application_name = config.get_config("DEFAULT", "application_name")
logger = logging.getLogger(application_name)
cluster_id = config.get_config('NATS', 'cluster_id')
channel = config.get_config('NATS', 'channel')
client_id = str(os.getpid())


async def run(loop):
    """
    Async function for watching messages in NATS.

    :param loop:
    """

    nc = NATS()
    sc = STAN()

    # Start session with NATS Streaming cluster using the established NATS connection.
    await nc.connect(io_loop=loop)

    await sc.connect(cluster_id=cluster_id, client_id=application_name + "_" + client_id, nats=nc)
    logger.info("Connected to NATS streaming server")

    # Async subscriber
    async def cb(msg):
        logger.info("Received a message (seq={}): {}".format(msg.seq, json.loads(msg.data)))
        worker.run(json.loads(msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe(subject=channel, durable_name=application_name, queue=application_name, start_at="first", cb=cb,
                       ack_wait=10)
