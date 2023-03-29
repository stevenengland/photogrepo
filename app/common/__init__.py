# from django.conf import settings


from app.common.ioc_containers import Container

container = Container()
# container.config.from_dict(settings.__dict__)
container.config.from_dict(
    {
        "PHOTOS_TEST": "TEST!123",
    },
)
