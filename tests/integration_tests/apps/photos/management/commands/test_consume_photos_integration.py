import os
from io import StringIO

import pytest
from django.conf import settings
from django.core.management import call_command

from app.photos.models import Photo
from tests.file_system_helper import FakeFileSystemHelper


@pytest.fixture(scope="function", autouse=True, name="cffs")
def consume_fake_fs(test_assets_fs: FakeFileSystemHelper):
    test_assets_fs.file_system.create_dir(
        test_assets_fs.test_assets_path.joinpath("repo"),
    )
    settings.PHOTOS_REPO_ROOTDIR = str(test_assets_fs.test_assets_path.joinpath("repo"))
    return test_assets_fs


def call_test_command(*args, **kwargs) -> tuple[str, str]:
    out = StringIO()
    err = StringIO()
    call_command(
        "consume_photos",
        *args,
        stdout=out,
        stderr=err,
        **kwargs,
    )
    return (out.getvalue(), err.getvalue())


@pytest.mark.django_db
def test_consume_photos_should_consume_2_photos_when_2_photos_are_in_consume_dir(  # noqa: WPS218
    cffs: FakeFileSystemHelper,
):
    settings.PHOTOS_CONSUME_ROOTDIR = str(
        cffs.test_assets_path.joinpath(
            "consume_photos",
            "multiple_photos",
        ),
    )

    out, err = call_test_command()

    # Test db entries
    photos = Photo.objects.all()
    assert photos.count() == 2

    # Test files are copied to repo
    files_it_repo = os.scandir(settings.PHOTOS_REPO_ROOTDIR)  # type: ignore[misc]
    files_repo = []
    for file_it_repo in files_it_repo:
        files_repo.append(file_it_repo.path)
    assert len(files_repo) == 2
    assert any("img01" in file_full_path for file_full_path in files_repo)
    assert any("img02" in file_full_path for file_full_path in files_repo)

    # Test src files are deleted from consume folder
    files_it_consume = os.scandir(settings.PHOTOS_CONSUME_ROOTDIR)  # type: ignore[misc]
    files_consume = []
    for file_it_consume in files_it_consume:
        files_consume.append(file_it_consume.path)
    assert not files_consume
