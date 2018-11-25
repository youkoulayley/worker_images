import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN


async def run(loop):
    # Use borrowed connection for NATS then mount NATS Streaming
    # client on top.
    nc = NATS()
    await nc.connect(io_loop=loop)

    # Start session with NATS Streaming cluster.
    sc = STAN()
    await sc.connect("serieall", "client-123", nats=nc)

    total_messages = 0
    future = asyncio.Future(loop=loop)

    async def cb(msg):
        nonlocal future
        nonlocal total_messages
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))
        total_messages += 1
        if total_messages >= 2:
            future.set_result(None)

    # Subscribe to get all messages since beginning.
    sub = await sc.subscribe("foo", start_at='first', cb=cb)
    await asyncio.wait_for(future, 1, loop=loop)

    # Stop receiving messages
    await sub.unsubscribe()

    # Close NATS Streaming session
    await sc.close()

    # We are using a NATS borrowed connection so we need to close manually.
    await nc.close()
