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
