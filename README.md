#  _EVENTOR_
Lightweight implementation of the Publisher/Subscriber pattern.

```python
import asyncio
import datetime as dt
from dataclasses import dataclass

from eventor import event_bus


async def main() -> None:

    @dataclass(frozen=True)
    class UserCreatedDomainEvent:
        user_id: str
        name: str
        created_at: dt.datetime

    @event_bus.handler()
    async def email_user_created_event_handler(event: UserCreatedDomainEvent) -> None:
        print(f"Send email: <Hello, '{event.name}'>.")

    event = UserCreatedDomainEvent(user_id="1", name="Don McLean", created_at=dt.datetime.now())
    await event_bus.publish(event)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```



# Installation
```bash
pip install git+https://github.com/ergnoore/eventor.git@v0.0.1
```

# Usage
For the eventor, it does not matter how the event data-classes are implemented. It just delivers your object to the subscriber.

Events are routed by name (_str_). The _eventor_ is trying to get a name from:

1. The name of the '_event_' argument type from the handler signature;
2. The name of the type specified in the _event_type_ argument;
2. The name specified in the _event_name_ argument;
##### Base usage (preferred method).

```python
import asyncio
import datetime as dt

from dataclasses import dataclass

from eventor import DefaultEventBus


async def main() -> None:

    event_bus = DefaultEventBus()
    @dataclass(frozen=True)
    class UserCreatedDomainEvent:
        user_id: str
        name: str
        created_at: dt.datetime

    async def email_user_created_event_handler(event: UserCreatedDomainEvent) -> None:
        print(f"Send email: <Hello, '{event.name}'>.")

    # The event name will be obtained from the annotation.
    subscription = event_bus.subscribe(email_user_created_event_handler)
    # or subscription = event_bus.subscribe(email_user_created_event_handler, event_type=UserCreatedDomainEvent)

    event = UserCreatedDomainEvent(user_id="1", name="Steve Buscemi", created_at=dt.datetime.now())

    await event_bus.publish(event)
    # or await event_bus.publish(event, event_type=UserCreatedDomainEvent) # Explicit caste of the event to the desired type.

    subscription.cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```



##### Publishing events without types

This method of publishing is implemented and is **not recommended** for use. You can probably forget to specify the name of the event and it will be published with the name: '_dict_'.
```python
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
```
