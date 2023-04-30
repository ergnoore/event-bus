from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Protocol,
    Type,
    TypeVar,
    overload,
)


__all__ = [
    "EventBus",
    "EventHandler",
    "EventBusSubscription",
]


E = TypeVar('E')


class EventHandler(Protocol):

    __slots__ = ()

    async def __call__(self, event: Any) -> None:
        raise NotImplementedError()


class EventBusSubscription(Generic[E]):

    __slots__ = ()

    @property
    def event_name(self) -> str:
        raise NotImplementedError()

    @property
    def event_type(self) -> Type[E]:
        raise NotImplementedError()

    @property
    def event_handler(self) -> EventHandler:
        raise NotImplementedError()

    def cancel(self) -> None:
        raise NotImplementedError()


class EventBus:

    __slots__ = ()

    async def publish(
        self,
        event: Any,
        event_type: Optional[Type] = None,
        event_name: Optional[str] = None,
    ) -> None:
        raise NotImplementedError()

    async def sync_publish(
        self,
        event: Any,
        event_type: Optional[Type] = None,
        event_name: Optional[str] = None,
    ) -> None:
        raise NotImplementedError()

    def handler(
        self,
        event_type: Optional[Type[E]] = None,
        event_name: Optional[str] = None
    ) -> Callable[[EventHandler], None]:
        raise NotImplementedError()

    @overload
    def subscribe(
        self,
        handler: EventHandler,
        event_type: Optional[Type[E]] = None
    ) -> EventBusSubscription[E]:
        ...

    @overload
    def subscribe(
        self,
        handler: EventHandler,
        event_name: str,
    ) -> EventBusSubscription:
        ...

    def subscribe(
        self,
        handler: EventHandler,
        event_type: Optional[Type[E]] = None,
        event_name: Optional[str] = None
    ) -> EventBusSubscription[E]:
        raise NotImplementedError()
