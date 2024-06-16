from asyncio import Task, CancelledError

from typing import Set


async def cancel_task(task: Task):
    """Cancel a task."""

    try:
        task.cancel()
        await task
    except CancelledError:
        pass

async def cancel_all(tasks: Set[Task]):
    """Cancel all tasks in a set."""

    for task in tasks:
        await cancel_task(task)