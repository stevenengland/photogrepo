from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.core.management.base import BaseCommand

from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)


@inject
class Command(BaseCommand):
    help = "Consumes all photo files in the consume directory."

    def __init__(
        self,
        logging_service: LoggingServiceInterface = Provide[  # noqa: WPS404
            "logging_service"
        ],
        photo_consumer_service: ConsumerServiceInterface = Provide[  # noqa: WPS404
            "photo_consumer_service"
        ],
    ) -> None:
        self.logging_service = logging_service
        self.photo_consumer_service = photo_consumer_service
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument("--runonce", action="store_true", help="Run only once.")

    def handle(self, *args, **options) -> None:  # noqa: WPS110
        self.logging_service.log_info("Starting consumption.")
        try:
            self.photo_consumer_service.consume_dir(
                settings.PHOTOS_CONSUME_ROOTDIR,  # type: ignore[misc]
                settings.PHOTOS_CONSUME_RECURSIVE,  # type: ignore[misc]
            )
        except Exception as exc:
            self.logging_service.log_error(
                f"Consume failed for one or more images: {str(exc)}",
            )
            raise exc

        if options["runonce"]:
            return
