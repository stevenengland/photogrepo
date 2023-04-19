import abc


class LoggingServiceInterface(abc.ABC):
    @abc.abstractmethod
    def log_info(self, message: str) -> None:
        pass
