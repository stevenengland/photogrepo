from dependency_injector import containers, providers

from app.common.services.file_system_service import FileSystemService
from app.common.services.logging_service import LoggingService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    file_system_service = providers.Factory(FileSystemService)
    logging_service = providers.Singleton(LoggingService)
