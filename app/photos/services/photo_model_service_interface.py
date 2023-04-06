from abc import ABC, abstractmethod

from app.photos.models import Photo


class PhotoModelServiceInterface(ABC):
    @abstractmethod
    def photo_create(self, dest_file_path: str, hash_md5: str) -> Photo:
        pass
