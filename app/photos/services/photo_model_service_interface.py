from abc import ABC, abstractmethod

from app.photos.models import Photo


class PhotoModelServiceInterface(ABC):
    @abstractmethod
    def photo_create(  # noqa: WPS211
        self,
        dest_file_path: str,
        hash_md5: str,
        hash_perceptual: str,
        hash_difference: str,
        hash_average: str,
        hash_wavelet: str,
    ) -> Photo:
        pass
