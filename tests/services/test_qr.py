import pytest
from app.services.qr import QrGeneratorService
from PIL import Image


def test_generate_qr_image():
    """Test generating a QR code image."""
    service = QrGeneratorService()
    data = "https://example.com"
    img = service.generate_qr_image(data=data)

    assert img is not None
    assert hasattr(img, "size")
    assert img.size[0] > 0
    assert img.size[1] > 0
