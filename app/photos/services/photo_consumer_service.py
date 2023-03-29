from dependency_injector.wiring import Provide, inject

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)

# from app.common.ioc_containers import Container
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)

# from django.conf import settings


@inject
class PhotoConsumerService2(ConsumerServiceInterface):
    def __init__(
        self,
        file_system_service: FileSystemServiceInterface = Provide[
            "file_system_service"
        ],
    ) -> None:
        self.file_system_service = file_system_service

    def consume(self, src_file_path: str) -> None:
        # Do preparatory work
        # ...
        # Finally copy the photo to the destination
        pass

    def print_something(self) -> None:
        # myval: str = Provide[Container.config.PHOTOS_TEST]
        myval: str = Provide["config.PHOTOS_TEST"]
        print(myval)
        pass
