from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)


@inject
class Command(BaseCommand):
    help = "Consumes all photo files in the consume directory."
    photo_consumer_service: ConsumerServiceInterface = Provide["photo_consumer_service"]
    logging_service: LoggingServiceInterface = Provide["logging_service"]

    def handle(self, *args, **kwargs):  # noqa: WPS110
        self.logging_service.log_info("Starting consumption.")
        try:
            self.photo_consumer_service.consume_dir(
                settings.PHOTOS_CONSUME_ROOTDIR,  # type: ignore[misc]
                settings.PHOTOS_CONSUME_RECURSIVE,  # type: ignore[misc]
            )
        except Exception as exc:
            raise CommandError(f"Consume failed for one or more images.\n\n{str(exc)}")
