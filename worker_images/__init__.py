import asyncio
import errno
import os
from worker_images import nats_client, logger, config

original_folder = config.get_config("DEFAULT", "original_folder")


if __name__ == '__main__':
    # Setup logger
    logger.init_logging()

    # Setup directory
    if not os.path.exists(original_folder):
        try:
            os.makedirs(original_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop))
    loop.run_forever()
