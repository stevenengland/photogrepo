from app.common import hashers
from app.photos.services.photo_analyzer_service_interface import (
    PhotoAnalyzerServiceInterface,
)


class PhotoAnalyzerService(PhotoAnalyzerServiceInterface):
    def hash_md5(self, file_path: str) -> str:
        return hashers.get_md5(file_path)
