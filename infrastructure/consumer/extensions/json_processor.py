from json import loads, JSONDecodeError

from aio_pika import IncomingMessage


def process_as_json(message: IncomingMessage):
    """process_as_json"""

    try:
        data = loads(message.body.decode())
        if not isinstance(data, dict): raise TypeError
    except (JSONDecodeError, TypeError):
        return False, {}
    return True, data