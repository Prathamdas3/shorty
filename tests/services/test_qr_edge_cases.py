"""Tests for QR code generator service error handling."""

import pytest
from app.services.qr import QrGeneratorService
from app.core.exception import AppException
from unittest.mock import patch, MagicMock


def test_qr_generator_initialization_success():
    """Test QrGeneratorService initializes successfully."""
    service = QrGeneratorService(
        version=None,
        border=4,
        box_size=10,
    )
    assert service._qr is not None


def test_qr_generator_initialization_with_version():
    """Test QrGeneratorService with specific version."""
    service = QrGeneratorService(version=1)
    assert service._qr is not None


def test_qr_generator_initialization_custom_params():
    """Test QrGeneratorService with custom parameters."""
    service = QrGeneratorService(
        version=5,
        border=10,
        box_size=20,
    )
    assert service._qr is not None


def test_qr_generator_initialization_error_correction():
    """Test QrGeneratorService with different error correction levels."""
    import qrcode

    levels = [
        qrcode.ERROR_CORRECT_L,
        qrcode.ERROR_CORRECT_M,
        qrcode.ERROR_CORRECT_Q,
        qrcode.ERROR_CORRECT_H,
    ]

    for level in levels:
        service = QrGeneratorService(error_correction=level)
        assert service._qr is not None


def test_qr_generator_generate_image_success():
    """Test generate_qr_image creates image successfully."""
    service = QrGeneratorService()

    image = service.generate_qr_image("https://example.com")

    assert image is not None
    assert hasattr(image, "size")
    assert image.size[0] > 0
    assert image.size[1] > 0


def test_qr_generator_generate_image_custom_colors():
    """Test generate_qr_image with custom colors."""
    service = QrGeneratorService()

    image = service.generate_qr_image(
        "https://example.com",
        back_color="red",
        fill_color="blue",
    )

    assert image is not None
    assert image.size[0] > 0


def test_qr_generator_generate_image_different_data():
    """Test generate_qr_image with different data types."""
    service = QrGeneratorService()

    test_data = [
        "https://example.com",
        "http://test.com/path",
        "Simple text",
        "123456789",
        "user@email.com",
    ]

    for data in test_data:
        image = service.generate_qr_image(data)
        assert image is not None


def test_qr_generator_generate_image_special_characters():
    """Test generate_qr_image with special characters."""
    service = QrGeneratorService()

    special_data = "Hello 世界! Ñoñ ©"
    image = service.generate_qr_image(special_data)

    assert image is not None
    assert image.size[0] > 0


def test_qr_generator_generate_image_long_data():
    """Test generate_qr_image with long data."""
    service = QrGeneratorService()

    long_data = "A" * 1000
    image = service.generate_qr_image(long_data)

    assert image is not None
    assert image.size[0] > 0


def test_qr_generator_generate_image_unicode():
    """Test generate_qr_image with unicode emojis."""
    service = QrGeneratorService()

    emoji_data = "Hello 😀 🎉 🚀"
    image = service.generate_qr_image(emoji_data)

    assert image is not None
    assert image.size[0] > 0


def test_qr_generator_initialization_failure():
    """Test QrGeneratorService handles initialization errors."""
    with patch("app.services.qr.qrcode.QRCode", side_effect=Exception("Init failed")):
        with pytest.raises(AppException) as exc_info:
            QrGeneratorService()
        assert "Failed to initialize QR code generator" in str(exc_info.value)


def test_qr_generator_generate_image_failure():
    """Test generate_qr_image handles generation errors."""
    service = QrGeneratorService()

    with patch.object(
        service._qr, "add_data", side_effect=Exception("Add data failed")
    ):
        with pytest.raises(AppException) as exc_info:
            service.generate_qr_image("test")
        assert "Failed to generate QR code" in str(exc_info.value)


def test_qr_generator_make_image_failure():
    """Test generate_qr_image handles make_image errors."""
    service = QrGeneratorService()

    with patch.object(service._qr, "make", side_effect=Exception("Make failed")):
        with pytest.raises(AppException) as exc_info:
            service.generate_qr_image("test")
        assert "Failed to generate QR code" in str(exc_info.value)


def test_qr_generator_multiple_qr_codes():
    """Test generating multiple QR codes."""
    service = QrGeneratorService()

    urls = [
        "https://example1.com",
        "https://example2.com",
        "https://example3.com",
    ]

    for url in urls:
        image = service.generate_qr_image(url)
        assert image is not None
        assert image.size[0] > 0


def test_qr_generator_box_size_impact():
    """Test box_size parameter affects image size."""
    service_small = QrGeneratorService(box_size=5)
    service_large = QrGeneratorService(box_size=20)

    image_small = service_small.generate_qr_image("test")
    image_large = service_large.generate_qr_image("test")

    assert image_large.size[0] > image_small.size[0]
    assert image_large.size[1] > image_small.size[1]


def test_qr_generator_border_parameter():
    """Test border parameter affects QR code."""
    service_no_border = QrGeneratorService(border=0)
    service_with_border = QrGeneratorService(border=10)

    image_no_border = service_no_border.generate_qr_image("test")
    image_with_border = service_with_border.generate_qr_image("test")

    assert image_no_border is not None
    assert image_with_border is not None


def test_qr_generator_different_versions():
    """Test different QR code versions."""
    for version in range(1, 5):
        service = QrGeneratorService(version=version)
        image = service.generate_qr_image("test")
        assert image is not None
        assert image.size[0] > 0


def test_qr_generator_empty_data():
    """Test generate_qr_image with empty data."""
    service = QrGeneratorService()

    image = service.generate_qr_image("")
    assert image is not None


def test_qr_generator_url_with_query_params():
    """Test generate_qr_image with URLs containing query parameters."""
    service = QrGeneratorService()

    url = "https://example.com?param1=value1&param2=value2"
    image = service.generate_qr_image(url)

    assert image is not None
    assert image.size[0] > 0
