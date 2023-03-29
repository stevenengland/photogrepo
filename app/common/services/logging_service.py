from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)


class LoggingService(LoggingServiceInterface):
    def log(self, message: str) -> None:
        print(message)  # noqa: WPS421
