from django.apps import AppConfig


class CommonConfig(AppConfig):
    """The config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.photos"
