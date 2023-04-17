from datetime import datetime

from app.common.services.file_name_generator_service_interface import (
    FileNameGeneratorServiceInterface,
)


class FileNameGeneratorService(FileNameGeneratorServiceInterface):
    def create_with_date_postfix(self, filename: str) -> str:
        filename_parts = filename.split(".", 1)
        uniqueness = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{filename_parts[0]}_{uniqueness}.{filename_parts[1]}"
