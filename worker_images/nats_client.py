import logging
import json
import os
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
from worker_images import worker

logger = logging.getLogger('worker_images')
client_id = str(os.getpid())


async def run(loop, conf):
    """
    Async function for watching messages in NATS.

    :param conf:
    :param loop:
    """
    cluster_id = conf.get('NATS', 'cluster_id')
    connection_name = conf.get('NATS', 'connection_name')
    channel = conf.get('NATS', 'channel')
    worker_image = worker.WorkerImage(conf)

    nc = NATS()
    sc = STAN()

    # Start session with NATS Streaming cluster using the established NATS connection.
    await nc.connect(io_loop=loop)

    await sc.connect(cluster_id=cluster_id, client_id=connection_name + "_" + client_id, nats=nc)
    logger.info("Connected to NATS streaming server")

    # Async subscriber
    async def cb(msg):
        logger.info("Received a message (seq={}): {}".format(msg.seq, json.loads(msg.data)))
        worker_image.run(json.loads(msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe(subject=channel, durable_name=connection_name, queue=connection_name, start_at="first", cb=cb,
                       ack_wait=10)
