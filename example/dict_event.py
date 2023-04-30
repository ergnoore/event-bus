import asyncio

from typing import Any
from typing import Mapping

from eventor import event_bus


async def main() -> None:

    async def event_handler(data: Mapping[str, Any]) -> None:
        print(f"Handle mapping event: '{data}'.")

    subscription = event_bus.subscribe(event_handler, event_name="DictEvent")
    await event_bus.publish({"foo": "bar"}, event_name="DictEvent")
    subscription.cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
