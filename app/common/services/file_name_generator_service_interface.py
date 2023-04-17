import abc


class FileNameGeneratorServiceInterface(abc.ABC):
    @abc.abstractmethod
    def create_with_date_postfix(self, filename: str) -> str:
        pass
