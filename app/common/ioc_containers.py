from dependency_injector import containers, providers

from app.common.services.file_system_service import FileSystemService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    file_system_service = providers.Factory(FileSystemService)
