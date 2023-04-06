import pytest

from app.photos.models import Photo


# Very basic db test. More model related db tests are located in the corresponding model service test file.
@pytest.mark.django_db
def test_photo_can_be_created():
    photo = Photo.objects.create(dest_file_path="test")

    assert photo.dest_file_path == "test"
    assert Photo.objects.count() == 1
