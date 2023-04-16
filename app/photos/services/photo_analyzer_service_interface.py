from abc import ABC, abstractmethod


class PhotoAnalyzerServiceInterface(ABC):
    @abstractmethod
    def hash_md5(self, file_path: str) -> str:
        pass

    @abstractmethod
    def hash_perceptual(self, file_path: str) -> str:
        pass

    @abstractmethod
    def hash_difference(self, file_path: str) -> str:
        pass

    @abstractmethod
    def hash_average(self, file_path: str) -> str:
        pass

    @abstractmethod
    def hash_wavelet(self, file_path: str) -> str:
        pass

    @abstractmethod
    def encoding_cnn(self, file_path: str) -> str:
        pass

    @abstractmethod
    def validate_image(self, file_path: str, extended_checks: bool = False) -> None:
        pass
