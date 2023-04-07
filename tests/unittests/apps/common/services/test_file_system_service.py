import shutil

import pytest
from pytest_mock import MockerFixture

from app.common.services import file_system_service


def test_copying_file_succeeds_if_path_does_not_exist(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.common.services.file_system_service.path.exists",
        return_value=False,
    )
    mocker.patch(
        "app.common.services.file_system_service.path.abspath",
        return_value="/testdir",
    )
    mocker.patch("app.common.services.file_system_service.makedirs")
    mocker.patch("app.common.services.file_system_service.shutil.copy2")
    fss = file_system_service.FileSystemService()

    fss.copy_file("testsrc", "testdst")

    file_system_service.makedirs.assert_called_once_with("/", exist_ok=True)  # type: ignore[attr-defined]
    file_system_service.shutil.copy2.assert_called_once_with(  # type: ignore[attr-defined]
        src="testsrc",
        dst="testdst",
    )


def test_copying_file_succeeds_if_path_exists(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.common.services.file_system_service.path.exists",
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
