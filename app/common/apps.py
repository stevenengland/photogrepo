from django.apps import AppConfig

from app.common import container


class CommonConfig(AppConfig):
    """The config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.common"

    def ready(self) -> None:
        container.wire(
            modules=["app.photos.services.photo_consumer_service"],
            packages=[
                # "app.common",
                #    "app.photos",
            ],
        )
