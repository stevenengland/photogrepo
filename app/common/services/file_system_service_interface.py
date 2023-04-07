import abc


class FileSystemServiceInterface(abc.ABC):
    @abc.abstractmethod
    def copy_file(self, src_file_path: str, dst_file_path: str) -> None:
        pass

    @abc.abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass
