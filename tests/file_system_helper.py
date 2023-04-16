from pathlib import PurePath

from pyfakefs.fake_filesystem import FakeFilesystem


class FakeFileSystemHelper(object):
    def __init__(self, test_assets_path: PurePath, file_system: FakeFilesystem) -> None:
        self._test_assets_path = test_assets_path
        self._file_system = file_system

    @property
    def test_assets_path(self) -> PurePath:
        return self._test_assets_path

    @property
    def file_system(self) -> FakeFilesystem:
        return self._file_system
