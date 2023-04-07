import os
import shutil

import pytest
from pytest_mock import MockerFixture

from app.common import hashers
from app.common.services import file_system_service


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
