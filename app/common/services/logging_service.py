import structlog

from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)


class LoggingService(LoggingServiceInterface):
    def __init__(
        self,
    ) -> None:
        self.logger = structlog.get_logger()

    def log_info(self, message: str) -> None:
        self.logger.info(message)
