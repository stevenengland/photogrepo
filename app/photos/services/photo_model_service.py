from django.db import transaction

from app.photos.models import Photo
from app.photos.services.photo_model_service_interface import (
    PhotoModelServiceInterface,
)


class PhotoModelService(PhotoModelServiceInterface):
    @transaction.atomic
    def photo_create(  # noqa: WPS211
        self,
        dest_file_path: str,
        hash_md5: str,
        hash_perceptual: str,
        hash_difference: str,
        hash_average: str,
        hash_wavelet: str,
    ) -> Photo:
        photo = Photo(
            dest_file_path=dest_file_path,
            hash_md5=hash_md5,
            hash_perceptual=hash_perceptual,
            hash_difference=hash_difference,
            hash_average=hash_average,
            hash_wavelet=hash_wavelet,
        )
        photo.full_clean()
        photo.save()

        return photo
