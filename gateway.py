import logging.config

import asyncio as aio

from integration import run_gateway


logging.config.fileConfig('logger.conf')


if __name__ == '__main__':
    loop = aio.new_event_loop()
    aio.set_event_loop(loop)

    try:
        gateway_coroutine = run_gateway(loop)
        loop.run_until_complete(gateway_coroutine)
        loop.run_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping event loop.")
        loop.stop()
    finally:
        loop.close()