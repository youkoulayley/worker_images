import asyncio
from worker_images import nats_client, logger, config

if __name__ == '__main__':
    logger.init_logging()
    config.init_config()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop))
    loop.run_forever()
