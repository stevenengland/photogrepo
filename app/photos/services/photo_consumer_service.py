from django.conf import settings

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)


class PhotoConsumerService(ConsumerServiceInterface):
    def __init__(self, file_system_service: FileSystemServiceInterface) -> None:
        self.file_system_service = file_system_service

    def consume(self, src_file_path: str) -> None:
        # Do preparatory work
        # ...
        # Finally copy the photo to the destination
        self.file_system_service.copy_file(
            src_file_path=src_file_path,
            dst_file_path=settings.PHOTOS_REPO_ROOTDIR,  # type: ignore[misc]
        )
