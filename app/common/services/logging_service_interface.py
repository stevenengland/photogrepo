import abc


class LoggingServiceInterface(abc.ABC):
    @abc.abstractmethod
    def log(self, message: str) -> None:
        pass
