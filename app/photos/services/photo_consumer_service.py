# from app.common.services.file_system_service_interface import (
#    FileSystemServiceInterface,
# )

from dependency_injector.wiring import Provide, as_int, inject

# from app.ioc_containers import Container
from app.photos.services.consumer_service_interface import (
    ConsumerServiceInterface,
)

# from django.conf import settings


@inject
class PhotoConsumerService2(ConsumerServiceInterface):
    def __init__(
        self,
        name,
    ) -> None:
        self.name = name

    def consume(self, src_file_path: str) -> None:
        # Do preparatory work
        # ...
        # Finally copy the photo to the destination
        pass

    @inject
    def print_something(self) -> None:
        # print(Provide[Container.config.PHOTOS_TEST])
        print(Provide["config.PHOTOS_TEST"])
        pass


# class PhotoConsumerService(ConsumerServiceInterface):
#    def __init__(self, file_system_service: FileSystemServiceInterface) -> None:
#        self.file_system_service = file_system_service
#
#    def consume(self, src_file_path: str) -> None:
#        # Do preparatory work
#        # ...
#        # Finally copy the photo to the destination
#        self.file_system_service.copy_file(
#            src_file_path=src_file_path,
#            dst_file_path=settings.PHOTOS_REPO_ROOTDIR,  # type: ignore[misc]
#        )
#


# @inject
# class PhotoConsumerService2(ConsumerServiceInterface):
#    def __init__(
#        self,
#        file_system_service: FileSystemServiceInterface = Provide[
#            Container.photo_consumer_service
#        ],
#    ) -> None:
#        self.file_system_service = file_system_service
#
#    def consume(self, src_file_path: str) -> None:
#        # Do preparatory work
#        # ...
#        # Finally copy the photo to the destination
#        self.file_system_service.copy_file(
#            src_file_path=src_file_path,
#            dst_file_path=Provide[Container.config.PHOTOS_REPO_ROOTDIR],
#        )
#
#    def print_something(self) -> None:
#        print(Provide[Container.config.PHOTOS_TEST])


# @inject
# class PhotoConsumerService2:
#    def __init__(
#        self,
#        name,
#    ) -> None:
#        self.name = name
#
#    def consume(self, src_file_path: str) -> None:
#        # Do preparatory work
#        # ...
#        # Finally copy the photo to the destination
#        pass
#
#    def print_something(self) -> None:
#        # print(Provide[Container.config.PHOTOS_TEST])
#        pass
