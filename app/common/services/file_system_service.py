import os
import shutil

from app.common import hashers
from app.common.exceptions import ApplicationError
from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)


class FileSystemService(FileSystemServiceInterface):
    def copy_file(self, src_file_path: str, dst_file_path: str) -> None:
        if not os.path.exists(dst_file_path):
            os.makedirs(
                os.path.dirname(os.path.abspath(dst_file_path)),
                exist_ok=True,
            )
        try:
            shutil.copy2(src=src_file_path, dst=dst_file_path)

        except shutil.SameFileError:
            raise ApplicationError("The same file already exists.")

        except PermissionError:
            raise ApplicationError("Permission denied.")

        except Exception:
            raise ApplicationError("Error occurred while copying file.")

        self._compare_hashes(src_file_path, dst_file_path)

    def delete_file(self, file_path: str) -> None:
        os.remove(file_path)

    def _compare_hashes(self, src_file_path: str, dst_file_path: str):
        pre_hash = hashers.get_md5(file_path=src_file_path)
        post_hash = hashers.get_md5(file_path=dst_file_path)
        if pre_hash != post_hash:
            os.remove(path=src_file_path)
            raise ApplicationError(
                "The hashes of the source file differs from the file copied to the target.",
            )
