import pytest
from django.conf import settings
from pytest_mock import MockerFixture

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.photos.services import photo_consumer_service


@pytest.fixture(scope="module", name="pcs_mock")
def photo_consumer_service_mock(
    mocker: MockerFixture,
) -> photo_consumer_service.PhotoConsumerService:
    file_system_service_mock = mocker.Mock(spec=FileSystemServiceInterface)
    pcs = photo_consumer_service.PhotoConsumerService(
        file_system_service=file_system_service_mock,
    )
    return pcs


# def test_consume_copies_file_to_destination(
#    pcs_mock: photo_consumer_service.PhotoConsumerService,
# ) -> None:
#    settings.PHOTOS_REPO_ROOTDIR = "/test"
#    mocked_copy_file = mocker.patch(
#        "app.common.services.file_system_service.FileSystemService.copy_file",
#    )
#
#    pcs_mock.print_something()
#    pcs_mock.consume(src_file_path="/test/test.jpg")
#
#    mocked_copy_file.assert_called_once_with(
#        src_file_path="/test/test.jpg",
#        dst_file_path="/test",
#    )


def test_consume_copies_file_to_destination2(mocker: MockerFixture) -> None:
    settings.PHOTOS_REPO_ROOTDIR = "/test"
    mocked_copy_file = mocker.patch(
        "app.common.services.file_system_service.FileSystemService.copy_file",
    )
    pcs = photo_consumer_service.PhotoConsumerService()

    pcs.print_something()
    pcs.consume(src_file_path="/test/test.jpg")

    mocked_copy_file.assert_called_once_with(
        src_file_path="/test/test.jpg",
        dst_file_path="/test",
    )
