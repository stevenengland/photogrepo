import filetype
from imagededup.methods import CNN, AHash, DHash, PHash, WHash
from PIL import Image

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

    def encoding_cnn(self, file_path: str) -> str:
        encoder = CNN()
        encoding = encoder.encode_image(file_path)
        return encoding.dumps().hex()

    def validate_image(self, file_path: str, extended_checks: bool = False) -> None:
        if not filetype.is_image(file_path):
            raise TypeError(f"{file_path} is not a valid image.")

        if not extended_checks:
            return

        image = Image.open(file_path)
        try:
            image.transpose(Image.FLIP_LEFT_RIGHT)
        except Exception:
            raise TypeError(f"{file_path} is a corrupted image.")
        finally:
            image.close()
