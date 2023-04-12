import numpy
import pytest
from imagededup.methods import CNN, AHash, DHash, PHash, WHash

from app.common import hashers
from app.photos.services.photo_analyzer_service import PhotoAnalyzerService


@pytest.fixture(scope="function", name="pas")
def photo_analyzer_service() -> PhotoAnalyzerService:
    service = PhotoAnalyzerService()
    return service  # noqa: WPS331


def test_analyzer_returns_md5_hash(pas: PhotoAnalyzerService, expect):
    expect(hashers).get_md5(...).thenReturn("testhash")

    assert pas.hash_md5("testfile") == "testhash"


def test_analyzer_returns_perceptual_hash(pas: PhotoAnalyzerService, expect):
    expect(PHash).encode_image(...).thenReturn("testhash")

    assert pas.hash_perceptual("testfile") == "testhash"


def test_analyzer_returns_difference_hash(pas: PhotoAnalyzerService, expect):
    expect(DHash).encode_image(...).thenReturn("testhash")

    assert pas.hash_difference("testfile") == "testhash"


def test_analyzer_returns_average_hash(pas: PhotoAnalyzerService, expect):
    expect(AHash).encode_image(...).thenReturn("testhash")

    assert pas.hash_average("testfile") == "testhash"


def test_analyzer_returns_wavelet_hash(pas: PhotoAnalyzerService, expect):
    expect(WHash).encode_image(...).thenReturn("testhash")

    assert pas.hash_wavelet("testfile") == "testhash"


@pytest.mark.timeout(20)
def test_analyzer_returns_cnn_encoding(pas: PhotoAnalyzerService, when):
    np_array = numpy.array([1, 2])
    when(CNN).encode_image(...).thenReturn(np_array)
    assert pas.encoding_cnn("testfile") == np_array.dumps().hex()
