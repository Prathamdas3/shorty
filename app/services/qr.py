import qrcode
from typing import Optional, Any
from app.core.logger import get_logger
from app.core.exception import AppException

logger = get_logger(__name__)


class QrGeneratorService:
    """
    Service class for generating QR codes using the qrcode library.

    Provides methods to create QR code images with customizable parameters.
    """

    def __init__(
        self,
        version: Optional[int] = None,
        border: int = 4,
        box_size: int = 10,
        error_correction=qrcode.ERROR_CORRECT_H,
    ):
        """
        Initialize the QR code generator with specified parameters.

        Args:
            version (Optional[int]): QR code version (1-40). None for auto-sizing.
            border (int): Border size around the QR code. Defaults to 4.
            box_size (int): Size of each box in the QR code. Defaults to 10.
            error_correction: Error correction level. Defaults to ERROR_CORRECT_H.

        Raises:
            AppException: If QR code initialization fails.
        """
        try:
            self._qr = qrcode.QRCode(
                version=version,
                border=border,
                error_correction=error_correction,
                box_size=box_size,
            )
        except Exception as e:
            logger.error(f"Failed to initialize QR code generator: {e}")
            raise AppException("Failed to initialize QR code generator")

    def generate_qr_image(
        self, data: Any, back_color: str = "white", fill_color: str = "black"
    ):
        """
        Generate a QR code image from the provided data.

        Args:
            data (Any): The data to encode in the QR code.
            back_color (str): Background color of the QR code. Defaults to "white".
            fill_color (str): Foreground color of the QR code. Defaults to "black".

        Returns:
            Image: PIL Image object of the generated QR code.

        Raises:
            AppException: If QR code generation fails.
        """
        try:
            self._qr.add_data(data=data)
            self._qr.make(fit=True)
            return self._qr.make_image(fill_color=fill_color, back_color=back_color)
        except Exception as e:
            logger.error(f"Failed to generate QR code: {e}")
            raise AppException("Failed to generate QR code")
