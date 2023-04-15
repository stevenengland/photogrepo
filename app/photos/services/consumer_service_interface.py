from abc import ABC, abstractmethod


class ConsumerServiceInterface(ABC):
    @abstractmethod
    def consume(self, src_file_path: str) -> None:
        pass

    @abstractmethod
    def consume_dir(self, src_dir_path: str, recursive: bool = False) -> None:
        pass
