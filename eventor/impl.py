from asyncio import create_task
from collections import defaultdict
from logging import Logger, getLogger

from typing import (
    Any,
    Callable,
    MutableMapping,
    MutableSet,
    Optional,
    Type,
    TypeVar,
    get_type_hints,
)

from .core import (
    EventBus,
    EventBusSubscription,
    EventHandler,
)


__all__ = ["DefaultEventBus"]


E = TypeVar('E')


class DefaultEventBus(EventBus):

    __slots__ = (
        "__subscriptions",
        "__handlers",
        "__logger",
    )

    def __init__(self, logger: Optional[Logger] = None) -> None:
        self.__handlers: MutableMapping[str, MutableSet[EventHandler]] = defaultdict(set)
        self.__logger = logger or getLogger("eventor")

    async def __call_handler(self, event: E, handler: EventHandler) -> None:
        try:
            await handler(event)
        except Exception as exc:
            self.__logger.error(f"Error during event processing event: '{event}'.", exc_info=exc)

    async def publish(
        self,
        event: Any,
        event_type: Optional[Type] = None,
        event_name: Optional[str] = None
    ) -> None:
        event_type = event_type or type(event)
        event_name = event_name or (event_type.__name__ if event_type is not None else None)
        for handler in self.__handlers[event_name]:
            create_task(self.__call_handler(event, handler))
        self.__logger.debug(f"Event published (async): {repr(event)}.")

    async def sync_publish(
        self,
        event: Any,
        event_type: Optional[Type] = None,
        event_name: Optional[str] = None
    ) -> None:
        event_type = event_type or type(event)
        event_name = event_name or (event_type.__name__ if event_type is not None else None)
        for handler in self.__handlers[event_name]:
            await self.__call_handler(event, handler)
        self.__logger.debug(f"Event published (sync): {repr(event)}.")

    def __on_cancel(self, event_name: str, handler: EventHandler) -> None:
        self.__handlers[event_name].discard(handler)

    def subscribe(
        self,
        handler: EventHandler,
        event_type: Optional[Type[E]] = None,
        event_name: Optional[str] = None
    ) -> EventBusSubscription[E]:
        event_type = event_type or get_type_hints(handler).get("event", None)
        event_name = event_name or (event_type.__name__ if event_type is not None else None)
        if event_name is None:
            raise Exception(
                "The handler does not have an event type annotation and the event name is not specified."
            )
        self.__handlers[event_name].add(handler)
        return DefaultEventBusSubscription(
            event_name=event_name,
            event_type=event_type,
            event_handler=handler,
            on_cancel=self.__on_cancel,
        )

    def handler(
        self,
        event_type: Optional[Type[E]] = None,
        event_name: Optional[str] = None
    ) -> Callable[[EventHandler], None]:
        def wrapper(handler: EventHandler):
            self.subscribe(handler, event_type=event_type, event_name=event_name)
        return wrapper


class DefaultEventBusSubscription(EventBusSubscription[E]):

    __slots__ = (
        "__event_name",
        "__event_type",
        "__event_handler",
        "__on_cancel",
    )

    def __init__(
        self,
        event_name: str,
        event_type: Type[E],
        event_handler: EventHandler,
        on_cancel: Callable[[str, EventHandler], None]
    ) -> None:
        self.__event_name = event_name
        self.__event_type = event_type
        self.__event_handler = event_handler
        self.__on_cancel = on_cancel
    @property
    def event_name(self) -> str:
        return self.__event_name

    @property
    def event_type(self) -> Type[E]:
        return self.__event_type

    @property
    def event_handler(self) -> EventHandler:
        return self.__event_handler

    def cancel(self) -> None:
        self.__on_cancel(self.__event_name, self.__event_handler)

    def __repr__(self) -> str:
        return f"Subscription(name: {self.__event_name}, type: {self.__event_type}, handler: {self.__event_handler})"
