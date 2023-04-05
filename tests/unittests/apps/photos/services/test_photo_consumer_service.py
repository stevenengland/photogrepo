import pytest
from django.conf import settings
from mockito import mock

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)
from app.photos.services.photo_consumer_service import PhotoConsumerService


@pytest.fixture(scope="module", name="pcs")
def photo_consumer_service() -> PhotoConsumerService:
    file_system_service_mock = mock(spec=FileSystemServiceInterface)
    logging_service_mock = mock(LoggingServiceInterface, strict=False)
    pcs = PhotoConsumerService(
        logging_service=logging_service_mock,
        file_system_service=file_system_service_mock,
    )
    return pcs  # noqa: WPS331


def test_consume_copies_file_to_destination(expect) -> None:
    settings.PHOTOS_REPO_ROOTDIR = "/test"
    fss_mock = mock(FileSystemServiceInterface)
    expect(fss_mock, times=1).copy_file(
        src_file_path="/test/test.jpg",
        dst_file_path="/test",
    )
    pcs = PhotoConsumerService(
        file_system_service=fss_mock,
    )

    pcs.consume(src_file_path="/test/test.jpg")


def test_consume_copies_file_to_destination2(pcs: PhotoConsumerService, expect):
    settings.PHOTOS_REPO_ROOTDIR = "/test"

    expect(pcs.file_system_service, times=1).copy_file(
        src_file_path="/test/test.jpg",
        dst_file_path="/test",
    )

    pcs.consume(src_file_path="/test/test.jpg")
