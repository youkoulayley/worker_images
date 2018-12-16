import asyncio
import errno
import argparse
import os
from worker_images import nats_client, logger, config


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Worker images resize & crop image.')
    parser.add_argument('-c', '--config-file', dest='config_file', default='config.ini', required=True,
                        help="Provide config file for the application")
    args = parser.parse_args()

    # Load configuration
    conf = config.load_config(args.config_file)
    original_folder = conf.get('DEFAULT', 'original_folder')

    # Setup logger
    logger.init_logging(conf.get('LOGGING', 'level'))

    # Setup directory
    if not os.path.exists(original_folder):
        try:
            os.makedirs(original_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop, conf))
    loop.run_forever()
