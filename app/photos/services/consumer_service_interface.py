from abc import ABC, abstractmethod


class ConsumerServiceInterface(ABC):
    @abstractmethod
    def consume(self, src_file_path: str) -> None:
        pass
