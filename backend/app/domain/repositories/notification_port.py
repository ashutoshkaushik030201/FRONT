from abc import ABC, abstractmethod


class NotificationPort(ABC):
    """Stub port for the future real-time (WebSocket) notification engine. Not implemented yet."""

    @abstractmethod
    async def notify_maintenance_due(self, asset_id: str, message: str) -> None: ...
