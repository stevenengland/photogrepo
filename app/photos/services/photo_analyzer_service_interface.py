from abc import ABC, abstractmethod


class PhotoAnalyzerServiceInterface(ABC):
    @abstractmethod
    def hash_md5(self, file_path: str) -> str:
        pass
