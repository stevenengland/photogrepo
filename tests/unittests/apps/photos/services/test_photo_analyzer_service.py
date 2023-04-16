import filetype
import numpy
import pytest
from imagededup.methods import CNN, AHash, DHash, PHash, WHash
from mockito import mock
from PIL import Image

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


def test_analyzer_should_return_succeed_when_valid_image_file_was_provided(
    pas: PhotoAnalyzerService,
    when,
):
    when(filetype).is_image(...).thenReturn(True)
    pas.validate_image("/validimage.jpg", extended_checks=False)


def test_analyzer_should_raise_when_verificatoin_detects_an_invalid_image(
    pas: PhotoAnalyzerService,
    when,
):
    when(filetype).is_image(...).thenReturn(False)
    with pytest.raises(expected_exception=TypeError, match="valid"):
        pas.validate_image("/invalidimage.jpg")


def test_analyzer_should_raise_when_extended_verificatoin_detects_an_invalid_image(
    pas: PhotoAnalyzerService,
    when,
):
    when(filetype).is_image(...).thenReturn(True)
    image = mock(Image.Image, strict=False)
    when(Image).open(...).thenReturn(image)
    when(image).transpose(...).thenRaise(Exception("test"))
    with pytest.raises(expected_exception=Exception, match="corrupted"):
        pas.validate_image("/invalidimage.jpg", extended_checks=True)
