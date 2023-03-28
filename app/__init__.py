from django.conf import settings

from app.ioc_containers import Container

container = Container()
container.config.from_dict(settings.__dict__)
