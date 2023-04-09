from dependency_injector.wiring import Provide, inject
from django.conf import settings

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)


@inject
class PhotoConsumerService(ConsumerServiceInterface):
    def __init__(
        self,
        logging_service: LoggingServiceInterface = Provide[  # noqa: WPS404
            "logging_service"
        ],
        file_system_service: FileSystemServiceInterface = Provide[  # noqa: WPS404
            "file_system_service"
        ],
    ) -> None:
        self.logging_service = logging_service
        self.file_system_service = file_system_service

    def consume(self, src_file_path: str) -> None:
        # Do preparatory work
        # ...
        # Finally copy the photo to the destination
        dst_file_path = settings.PHOTOS_REPO_ROOTDIR  # type: ignore[misc]
        self.logging_service.log_info(
            f"Copying file from {src_file_path} to {dst_file_path}",
        )
        self.file_system_service.copy_file(
            src_file_path=src_file_path,
            dst_file_path=dst_file_path,
        )

        self.file_system_service.delete_file(src_file_path)
