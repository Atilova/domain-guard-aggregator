from asyncio import Event

from typing import (
    TypedDict,
    TypeVar,
    Generic,
    Optional,
    Dict
)


K = TypeVar('K')
V = TypeVar('V')


class QueueItem(TypedDict, Generic[V]):
    """Represents an item in the AsyncKeyQueue."""

    event: Event
    result: Optional[V]


class AsyncKeyQueue(Generic[K, V]):
    """An asynchronous queue that waits for specific keys."""

    def __init__(self):
        self.__queue_items: Dict[K, QueueItem[V]] = {}

    async def place(self, key: K) -> Event:
        """Place a key in the queue."""

        if key in self.__queue_items:
            raise KeyError(f'The key "{key}" already exists in the queue.')

        event = Event()
        self.__queue_items[key] = { 'event': event, 'result': None }

        return event

    async def set(self, key: K, result: V) -> None:
        """Set the result for a given key."""

        if key not in self.__queue_items:
            raise KeyError(f'The key "{key}" was not found in the queue.')

        self.__queue_items[key]['result'] = result
        self.__queue_items[key]['event'].set()

    async def get(self, key: K) -> Optional[V]:
        """Get the result for a given key."""

        if key not in self.__queue_items:
            raise KeyError(f'The key "{key}" was not found in the queue.')

        item = self.__queue_items[key]
        await item['event'].wait()
        result = item['result']
        del self.__queue_items[key]
        return result
    
    @property
    def length(self) -> int:
        """Retrieve number of items in queue."""

        return len(self.__queue_items)