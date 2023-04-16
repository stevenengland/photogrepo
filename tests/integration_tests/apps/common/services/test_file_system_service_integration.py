import pytest

from app.common.services import file_system_service
from config.settings.components import BASE_DIR
from tests.file_system_helper import FakeFileSystemHelper


@pytest.fixture(scope="function", name="fss")
def photo_consumer_service() -> file_system_service.FileSystemService:
    fss = file_system_service.FileSystemService()
    return fss  # noqa: WPS331


def test_get_files_in_dir_should_return_array_of_2_elements_when_2_files_are_in_dir(
    fss: file_system_service.FileSystemService,
    test_assets_fs: FakeFileSystemHelper,
):
    files = fss.get_files_in_dir(
        str(test_assets_fs.test_assets_path.joinpath("get_files_in_dir")),
    )

    assert len(files) == 2
    assert any("test1.txt" in file_full_path for file_full_path in files)
    assert any("test2.txt" in file_full_path for file_full_path in files)


def test_get_files_in_dir_should_return_array_of_3_elements_when_3_files_are_in_dir_and_subdir(
    fss: file_system_service.FileSystemService,
):
    files = fss.get_files_in_dir(
        str(BASE_DIR.joinpath("tests", "test_assets", "get_files_in_dir")),
        recursive=True,
    )

    assert len(files) == 3
    assert any("test1.txt" in file_full_path for file_full_path in files)
    assert any("test2.txt" in file_full_path for file_full_path in files)
    assert any("test3.txt" in file_full_path for file_full_path in files)
