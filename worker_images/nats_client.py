import logging
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

logger = logging.getLogger("worker_images")


async def run(loop):
    nc = NATS()
    sc = STAN()

    # Start session with NATS Streaming cluster using the established NATS connection.
    await nc.connect(io_loop=loop)

    logger.debug("Connecting to NATS streaming server")
    await sc.connect("serieall", "worker_image", nats=nc)
    logger.info("Connected to NATS streaming server")

    # Example async subscriber
    async def cb(msg):
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe("foo", durable_name="worker_images", start_at="first", cb=cb)
