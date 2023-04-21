from appdirs import AppDirs

from config.settings.components import config

special_dirs = AppDirs("photogrepo", "stevenengland")

DATA_ROOTDIR: str = config(
    "PHOTOGREPO_DATA_ROOTDIR",
    default=f"{special_dirs.user_data_dir}/data",
)

HOSTING_DOMAIN_NAME: str = config("PHOTOGREPO_HOSTING_DOMAIN_NAME", default="local.lan")

LOGGING_FILE: str = config(
    "PHOTOGREPO_LOGGING_FILE",
    default=f"{DATA_ROOTDIR}/logs/photogrepo.log",
)
LOGGING_LEVEL: str = config("PHOTOGREPO_LOGGING_LEVEL", default="info")

PHOTOS_CONSUME_RECURSIVE: bool = config(
    "PHOTOGREPO_PHOTOS_CONSUME_RECURSIVE",
    default=False,
)
PHOTOS_CONSUME_ROOTDIR: str = config(
    "PHOTOGREPO_PHOTOS_CONSUME_ROOTDIR",
    default=f"{special_dirs.user_data_dir}/consume",
)

PHOTOS_REPO_ROOTDIR: str = config(
    "PHOTOGREPO_PHOTOS_REPO_ROOT_DIR",
    default=f"{special_dirs.user_data_dir}/photos",
)

PHOTOS_TEST: int = config("PHOTOGREPO_PHOTOS_TEST", default=10, cast=int)

# When dir is None then a os dependent temp directory will be used.
TMP_ROOTDIR: str = config(
    "PHOTOGREPO_TMP_ROOTDIR",
    default=None,
)
