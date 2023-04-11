from imagededup.methods import AHash, DHash, PHash, WHash

from app.common import hashers
from app.photos.services.photo_analyzer_service_interface import (
    PhotoAnalyzerServiceInterface,
)


class PhotoAnalyzerService(PhotoAnalyzerServiceInterface):
    def hash_md5(self, file_path: str) -> str:
        return hashers.get_md5(file_path)

    def hash_perceptual(self, file_path: str) -> str:
        hasher = PHash()
        return hasher.encode_image(file_path)

    def hash_difference(self, file_path: str) -> str:
        hasher = DHash()
        return hasher.encode_image(file_path)

    def hash_average(self, file_path: str) -> str:
        hasher = AHash()
        return hasher.encode_image(file_path)

    def hash_wavelet(self, file_path: str) -> str:
        hasher = WHash()
        return hasher.encode_image(file_path)
