import shutil
from os import makedirs, path

from app.common.exceptions import ApplicationError
from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)


class FileSystemService(FileSystemServiceInterface):
    def copy_file(self, src_file_path: str, dst_file_path: str) -> None:
        if not path.exists(dst_file_path):
            makedirs(path.dirname(path.abspath(dst_file_path)), exist_ok=True)
        try:
            shutil.copy2(src=src_file_path, dst=dst_file_path)

        except shutil.SameFileError:
            raise ApplicationError("The same file already exists.")

        except PermissionError:
            raise ApplicationError("Permission denied.")

        except Exception:
            raise ApplicationError("Error occurred while copying file.")
