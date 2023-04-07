from abc import ABC, abstractmethod


class PhotoAnalyzerServiceInterface(ABC):
    @abstractmethod
    def hash(self, src_file_path: str) -> None:
        pass
