from dependency_injector import containers, providers

# from app.common.services.file_system_service import FileSystemService
from app.photos.services.photo_consumer_service import PhotoConsumerService2


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            # "app.common",
            "app.photos",
        ],
    )

    config = providers.Configuration()

    photo_consumer_service = providers.Factory(
        PhotoConsumerService2,
        name="sten"
        # file_system_service=FileSystemService,
    )
