from django.db import transaction

from app.photos.models import Photo
from app.photos.services.photo_model_service_interface import (
    PhotoModelServiceInterface,
)


class PhotoModelService(PhotoModelServiceInterface):
    @transaction.atomic
    def photo_create(self, dest_file_path: str, hash_md5: str) -> Photo:
        photo = Photo(dest_file_path=dest_file_path, hash_md5=hash_md5)
        photo.full_clean()
        photo.save()

        return photo
