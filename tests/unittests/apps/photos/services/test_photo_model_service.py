import pytest

from app.photos.models import Photo
from app.photos.services.photo_model_service import PhotoModelService


@pytest.fixture(scope="module", name="pms")
def photo_model_service() -> PhotoModelService:
    pcs = PhotoModelService()
    return pcs  # noqa: WPS331


# Very basic db test. More model related db tests are located in the corresponding model service test file.
@pytest.mark.django_db
def test_photo_can_be_created(pms: PhotoModelService):
    photo = pms.photo_create(dest_file_path="testpath", hash_md5="testmd5")

    assert photo.dest_file_path == "testpath"
    assert Photo.objects.count() == 1
