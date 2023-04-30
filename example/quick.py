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
