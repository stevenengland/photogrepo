import os
import shutil

import pytest
from pytest_mock import MockerFixture

from app.common import hashers
from app.common.services import file_system_service
from config.settings.components import BASE_DIR


@pytest.fixture(scope="module", name="fss")
def photo_consumer_service() -> file_system_service.FileSystemService:
    fss = file_system_service.FileSystemService()
    return fss  # noqa: WPS331


def test_copying_file_succeeds_if_path_does_not_exist(
    when,
    mocker: MockerFixture,
) -> None:
    when(hashers).get_md5(...)
    mocker.patch(
        "app.common.services.file_system_service.os.path.exists",
        return_value=False,
    )
    mocker.patch(
        "app.common.services.file_system_service.os.path.abspath",
        return_value="/testdir",
    )
    mocker.patch("app.common.services.file_system_service.os.makedirs")
    mocker.patch("app.common.services.file_system_service.shutil.copy2")
    fss = file_system_service.FileSystemService()

    fss.copy_file("testsrc", "testdst")

    file_system_service.os.makedirs.assert_called_once_with("/", exist_ok=True)  # type: ignore[attr-defined]
    file_system_service.shutil.copy2.assert_called_once_with(  # type: ignore[attr-defined]
        src="testsrc",
        dst="testdst",
    )


def test_copying_file_succeeds_if_path_exists(
    when,
    mocker: MockerFixture,
) -> None:
    when(hashers).get_md5(...)
    mocker.patch(
        "app.common.services.file_system_service.os.path.exists",
        return_value=True,
    )
    mocked_copy = mocker.patch("app.common.services.file_system_service.shutil.copy2")
    fss = file_system_service.FileSystemService()

    fss.copy_file("testsrc", "testdst")

    mocked_copy.assert_called_once_with(src="testsrc", dst="testdst")


def test_copy_throws_if_file_already_exists(when):
    when(shutil).copy2(..., ...).thenRaise(shutil.SameFileError)
    with pytest.raises(expected_exception=Exception, match="already exists"):
        fss = file_system_service.FileSystemService()
        fss.copy_file("testsrc", "testdst")


def test_copy_throws_if_file_copied_has_wrong_hash(
    when,
    expect,
    fss: file_system_service.FileSystemService,
):
    expect(os, times=1).remove(...)
    when(shutil).copy2(..., ...)
    when(hashers).get_md5(...).thenReturn("first_hash").thenReturn("secondHash")
    with pytest.raises(expected_exception=Exception, match="hash"):
        fss.copy_file("testsrc", "testdst")


def test_delete_removes_file(
    expect,
    fss: file_system_service.FileSystemService,
):
    expect(os, times=1).remove(...)
    fss.delete_file("testdst")


def test_get_files_in_dir_should_return_array_of_2_elements_when_2_files_are_in_dir(
    fss: file_system_service.FileSystemService,
):
    files = fss.get_files_in_dir(
        str(BASE_DIR.joinpath("tests", "test_assets", "get_files_in_dir")),
    )

    assert len(files) == 2
    assert files[0].endswith("test1.txt")
    assert files[1].endswith("test2.txt")


def test_get_files_in_dir_should_return_array_of_3_elements_when_3_files_are_in_dir_and_subdir(
    fss: file_system_service.FileSystemService,
):
    files = fss.get_files_in_dir(
        str(BASE_DIR.joinpath("tests", "test_assets", "get_files_in_dir")),
        recursive=True,
    )

    assert len(files) == 3
    assert files[0].endswith("test1.txt")
    assert files[1].endswith("test2.txt")
    assert files[2].endswith("test3.txt")


def test_get_files_in_dir_should_throw_when_directory_is_invalid(
    fss: file_system_service.FileSystemService,
):
    with pytest.raises(expected_exception=Exception, match="is not a directory"):
        fss.get_files_in_dir("/testdirthatdoesnotexist")
