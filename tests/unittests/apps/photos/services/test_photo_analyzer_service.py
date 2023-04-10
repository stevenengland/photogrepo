import pytest

from app.common import hashers
from app.photos.services.photo_analyzer_service import PhotoAnalyzerService


@pytest.fixture(scope="function", name="pas")
def photo_analyzer_service() -> PhotoAnalyzerService:
    service = PhotoAnalyzerService()
    return service  # noqa: WPS331


def test_analyzer_returns_md5_hash(pas: PhotoAnalyzerService, expect):
    expect(hashers).get_md5(...).thenReturn("testhash")

    assert pas.hash_md5("testfile") == "testhash"
