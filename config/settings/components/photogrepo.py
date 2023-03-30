from appdirs import AppDirs

from config.settings.components import config

special_dirs = AppDirs("photogrepo", "stevenengland")

HOSTING_DOMAIN_NAME: str = config("PHOTOGREPO_HOSTING_DOMAIN_NAME", default="local.lan")

PHOTOS_REPO_ROOTDIR: str = config(
    "PHOTOGREPO_PHOTOS_REPO_ROOT_DIR",
    default=f"{special_dirs.user_data_dir}/photos",
)

PHOTOS_TEST: int = config("PHOTOGREPO_PHOTOS_TEST", default=10, cast=int)
