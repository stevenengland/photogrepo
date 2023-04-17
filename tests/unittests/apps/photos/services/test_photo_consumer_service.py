import pytest
from django.conf import settings
from mockito import mock, verify

from app.common.services.file_name_generator_service_interface import (
    FileNameGeneratorServiceInterface,
)
from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)
from app.photos.services.photo_analyzer_service import PhotoAnalyzerService
from app.photos.services.photo_consumer_service import PhotoConsumerService
from app.photos.services.photo_model_service_interface import (
    PhotoModelServiceInterface,
)


@pytest.fixture(scope="function", name="pcs")
def photo_consumer_service() -> PhotoConsumerService:
    file_system_service_mock = mock(FileSystemServiceInterface, strict=False)
    file_name_generator_service_mock = mock(
        FileNameGeneratorServiceInterface,
        strict=False,
    )
    logging_service_mock = mock(LoggingServiceInterface, strict=False)
    photo_model_service = mock(PhotoModelServiceInterface, strict=False)
    photo_analyzer_service = mock(PhotoAnalyzerService, strict=False)
    pcs = PhotoConsumerService(
        logging_service=logging_service_mock,
        file_system_service=file_system_service_mock,
        file_name_generator_service=file_name_generator_service_mock,
        photo_model_service=photo_model_service,
        photo_analyzer_service=photo_analyzer_service,
    )
    return pcs  # noqa: WPS331


def test_consume_copies_file_to_destination(pcs: PhotoConsumerService, expect, when):
    settings.PHOTOS_REPO_ROOTDIR = "/testtarget"
    when(pcs.file_name_generator_service).create_with_date_postfix(...).thenReturn(
        "test_20221001000000.jpg",
    )
    expect(pcs.file_system_service, times=1).copy_file(
        src_file_path="/test/test.jpg",
        dst_file_path="/testtarget/test_20221001000000.jpg",
    )

    pcs.consume(src_file_path="/test/test.jpg")


def test_consume_deletes_file_after_copy_finished(pcs: PhotoConsumerService, when):
    settings.PHOTOS_REPO_ROOTDIR = "/testtarget"
    when(pcs.file_name_generator_service).create_with_date_postfix(...).thenReturn(
        "test_20221001000000.jpg",
    )

    pcs.consume(src_file_path="/test/test.jpg")

    verify(pcs.file_system_service, inorder=True).copy_file(
        src_file_path="/test/test.jpg",
        dst_file_path="/testtarget/test_20221001000000.jpg",
    )

    verify(pcs.file_system_service, inorder=True).delete_file("/test/test.jpg")


def test_consume_creates_record_in_database(pcs: PhotoConsumerService, expect, when):
    settings.PHOTOS_REPO_ROOTDIR = "/testtarget"
    when(pcs.file_name_generator_service).create_with_date_postfix(...).thenReturn(
        "test_20221001000000.jpg",
    )
    expect(pcs.photo_analyzer_service).hash_md5(...).thenReturn(  # noqa: WPS204
        "md5",
    )
    expect(pcs.photo_analyzer_service).hash_perceptual(...).thenReturn("perceptual")
    expect(pcs.photo_analyzer_service).hash_difference(...).thenReturn("diff")
    expect(pcs.photo_analyzer_service).hash_average(...).thenReturn("avg")
    expect(pcs.photo_analyzer_service).hash_wavelet(...).thenReturn("wavelet")
    expect(pcs.photo_analyzer_service).encoding_cnn(...).thenReturn("cnn")

    pcs.consume(src_file_path="/test/test.jpg")

    verify(pcs.photo_model_service).photo_create(
        dest_file_path="/testtarget/test_20221001000000.jpg",
        hash_md5="md5",
        hash_perceptual="perceptual",
        hash_difference="diff",
        hash_average="avg",
        hash_wavelet="wavelet",
        encoding_cnn="cnn",
    )


def test_consume_dir_triggers_consume_for_each_file_in_dir(
    pcs: PhotoConsumerService,
    expect,
    when,
):
    when(pcs.file_system_service).get_files_in_dir(..., ...).thenReturn(
        ["/test/test1.jpg", "/test/test2.txt", "/test/test3.mpg"],
    )
    expect(pcs, times=3).consume(...)

    pcs.consume_dir("/test")


def test_consume_dir_should_not_stop_consuming_files_when_one_file_of_many_is_not_consumable(
    pcs: PhotoConsumerService,
    when,
):
    settings.PHOTOS_REPO_ROOTDIR = "/testtarget"
    when(pcs.file_name_generator_service).create_with_date_postfix(
        "test1.jpg",
    ).thenReturn(
        "test1_20221001000000.jpg",
    )
    when(pcs.file_name_generator_service).create_with_date_postfix(
        "test2.txt",
    ).thenReturn(
        "test2_20221001000000.txt",
    )
    when(pcs.file_name_generator_service).create_with_date_postfix(
        "test3.mpg",
    ).thenReturn(
        "test3_20221001000000.mpg",
    )
    when(pcs.file_system_service).get_files_in_dir(..., ...).thenReturn(
        ["/test/test1.jpg", "/test/test2.txt", "/test/test3.mpg"],
    )
    when(pcs.file_system_service).copy_file(
        src_file_path="/test/test1.jpg",
        dst_file_path="/testtarget/test1_20221001000000.jpg",
    )
    when(pcs.file_system_service).copy_file(
        src_file_path="/test/test2.txt",
        dst_file_path="/testtarget/test2_20221001000000.txt",
    ).thenRaise(Exception("test"))
    when(pcs.file_system_service).copy_file(
        src_file_path="/test/test3.mpg",
        dst_file_path="/testtarget/test3_20221001000000.mpg",
    )

    pcs.consume_dir("/test")
