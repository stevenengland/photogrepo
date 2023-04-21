import os

from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.db import transaction

from app.common.services.file_name_generator_service_interface import (
    FileNameGeneratorServiceInterface,
)
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
    def __init__(  # noqa: WPS211
        self,
        logging_service: LoggingServiceInterface = Provide[  # noqa: WPS404
            "logging_service"
        ],
        file_system_service: FileSystemServiceInterface = Provide[  # noqa: WPS404
            "file_system_service"
        ],
        file_name_generator_service: FileNameGeneratorServiceInterface = Provide[  # noqa: WPS404
            "file_name_generator_service"
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
        self.file_name_generator_service = file_name_generator_service
        self.photo_model_service = photo_model_service
        self.photo_analyzer_service = photo_analyzer_service

    def consume(self, src_file_path: str) -> None:
        self.logging_service.log_info(
            f"Consumtion started for {src_file_path}",
        )
        try:
            self._consume(src_file_path)
        except Exception as exc:
            self.logging_service.log_info(
                f"Consumtion afiled for {src_file_path} with error:\n\n{str(exc)}",
            )

    def consume_dir(self, src_dir_path: str, recursive: bool = False) -> None:
        self.logging_service.log_info(
            f"Consumtion started for {src_dir_path}",
        )

        files = self.file_system_service.get_files_in_dir(
            src_dir_path,
            recursive,
        )

        for photo_files in files:
            self.consume(photo_files)

    def _generate_unique_filename(self, filename: str) -> str:
        return self.file_name_generator_service.create_with_date_postfix(filename)

    def _consume(self, src_file_path: str) -> None:  # noqa: WPS210
        # Construct a few facts
        dst_file_path = self._construct_dst_file_path(src_file_path)
        tmp_dir_path = self.file_system_service.create_tmp_dir(settings.TMP_ROOTDIR)  # type: ignore[misc]
        tmp_file_path = f"{tmp_dir_path}/{os.path.basename(src_file_path)}"

        # Phase 1: Nothing to roll back if action fails
        self.file_system_service.copy_file(
            src_file_path=src_file_path,
            dst_file_path=tmp_file_path,
        )

        # Phase 2: If something fails, the tmp file needs to be deleted.
        # The transaction ensures that a commit is only executed if all other steps succeed.
        try:  # noqa: WPS229
            hash_md5 = self.photo_analyzer_service.hash_md5(tmp_file_path)
            hash_perceptual = self.photo_analyzer_service.hash_perceptual(tmp_file_path)
            hash_difference = self.photo_analyzer_service.hash_difference(tmp_file_path)
            hash_average = self.photo_analyzer_service.hash_average(tmp_file_path)
            hash_wavelet = self.photo_analyzer_service.hash_wavelet(tmp_file_path)
            encoding_cnn = self.photo_analyzer_service.encoding_cnn(tmp_file_path)
            with transaction.atomic():
                self.photo_model_service.photo_create(
                    dest_file_path=dst_file_path,
                    hash_md5=hash_md5,
                    hash_perceptual=hash_perceptual,
                    hash_difference=hash_difference,
                    hash_average=hash_average,
                    hash_wavelet=hash_wavelet,
                    encoding_cnn=encoding_cnn,
                )
                self.file_system_service.copy_file(
                    src_file_path=src_file_path,
                    dst_file_path=dst_file_path,
                )

                # The very last step: Delete the source...
                self.file_system_service.delete_file(src_file_path)
        except Exception as exc:
            self.logging_service.log_error(
                f"Consumtion failed with error {str(exc)}",
            )
        finally:
            self.file_system_service.delete_dir(tmp_dir_path)

    def _construct_dst_file_path(self, src_file_path: str) -> str:
        dst_file_name = self._generate_unique_filename(os.path.basename(src_file_path))
        return os.path.join(settings.PHOTOS_REPO_ROOTDIR, dst_file_name)  # type: ignore[misc]
