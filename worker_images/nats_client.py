import logging
import json
import os
import ssl
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
    servers = json.loads(conf.get('NATS', 'servers'))
    nats_tls = conf.getboolean('NATS', 'tls')
    cluster_id = conf.get('NATS', 'cluster_id')
    connection_name = conf.get('NATS', 'connection_name')
    channel = conf.get('NATS', 'channel')
    worker_image = worker.WorkerImage(conf)

    nc = NATS()
    sc = STAN()
    
    if nats_tls:
        # Load SSL configuration
        ca_cert = conf.get('NATS', 'ca_cert')
        client_cert = conf.get('NATS', 'client_cert')
        client_key = conf.get('NATS', 'client_key')

        # Prepare tls context
        tls_ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        tls_ctx.load_verify_locations(ca_cert)
        tls_ctx.load_cert_chain(certfile=client_cert,
                                keyfile=client_key)

        # Connect to NATS server with TLS
        await nc.connect(servers=servers, io_loop=loop, tls=tls_ctx)
        logger.info("Connected to NATS server with TLS.")
    else:
        # Connect to NATS server without TLS
        await nc.connect(servers=servers, io_loop=loop)
        logger.info("Connected to NATS server without TLS.")

    # Connect to NATS streaming server with NATS connection configured above
    await sc.connect(cluster_id=cluster_id, client_id=connection_name + "_" + client_id, nats=nc)
    logger.info("Connected to NATS streaming server")

    # Async subscriber
    async def cb(msg):
        logger.info("Received a message (seq={}): {}".format(msg.seq, json.loads(msg.data)))
        worker_image.run(json.loads(msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe(subject=channel, durable_name=connection_name, queue=connection_name, start_at="first", cb=cb,
                       ack_wait=10)
