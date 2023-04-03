from django.conf import settings
from pytest_mock import MockerFixture

from app.photos.services import photo_consumer_service


def test_consume_copies_file_to_destination(mocker: MockerFixture) -> None:
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
