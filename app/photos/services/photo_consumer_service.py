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
from app.photos.services.photo_analyzer_service_interface import (
    PhotoAnalyzerServiceInterface,
)
from app.photos.services.photo_model_service_interface import (
    PhotoModelServiceInterface,
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
        photo_model_service: PhotoModelServiceInterface = Provide[  # noqa: WPS404
            "photo_model_service"
        ],
        photo_analyzer_service: PhotoAnalyzerServiceInterface = Provide[  # noqa: WPS404
            "photo_analyzer_service"
        ],
    ) -> None:
        self.logging_service = logging_service
        self.file_system_service = file_system_service
        self.photo_model_service = photo_model_service
        self.photo_analyzer_service = photo_analyzer_service

    def consume(self, src_file_path: str) -> None:  # noqa: WPS210
        self.logging_service.log_info(
            f"Consumtion started for {src_file_path}",
        )
        dst_file_path = settings.PHOTOS_REPO_ROOTDIR  # type: ignore[misc]
        self.logging_service.log_info(
            f"Copying file from {src_file_path} to {dst_file_path}",
        )
        self.file_system_service.copy_file(
            src_file_path=src_file_path,
            dst_file_path=dst_file_path,
        )

        # After a successful copy action, gather facts from src file
        hash_md5 = self.photo_analyzer_service.hash_md5(src_file_path)
        hash_perceptual = self.photo_analyzer_service.hash_perceptual(src_file_path)
        hash_difference = self.photo_analyzer_service.hash_difference(src_file_path)
        hash_average = self.photo_analyzer_service.hash_average(src_file_path)
        hash_wavelet = self.photo_analyzer_service.hash_wavelet(src_file_path)
        encoding_cnn = self.photo_analyzer_service.encoding_cnn(src_file_path)

        self.logging_service.log_info(
            f"Deleting file {src_file_path}",
        )
        self.file_system_service.delete_file(src_file_path)
        self.logging_service.log_info(
            "Creating db entry for photo",
        )
        self.photo_model_service.photo_create(
            dest_file_path=dst_file_path,
            hash_md5=hash_md5,
            hash_perceptual=hash_perceptual,
            hash_difference=hash_difference,
            hash_average=hash_average,
            hash_wavelet=hash_wavelet,
            encoding_cnn=encoding_cnn,
        )
