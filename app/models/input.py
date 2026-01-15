from app.core.pydantic import CustomBaseModel
from pydantic import field_validator, AnyHttpUrl
from urllib.parse import urlparse
import ipaddress
import socket


class SortIDInput(CustomBaseModel):
    sort_id: str

    @field_validator("sort_id", mode="before")
    def check_id(cls, v, info):
        if not v:
            raise ValueError(f"{info.field_name} missing")

        if not isinstance(v, str):
            raise TypeError(f"{info.field_name} must be of type string")

        if not v.strip():
            raise ValueError(f"{info.field_name} can not be empty")

        if len(v) != 7:
            raise ValueError(f"{info.field_name} must be of length 7")

        return v


class OriginalUrlInput(CustomBaseModel):
    link: AnyHttpUrl

    @field_validator("link")
    def check_link(cls, v, info):
        parsed = urlparse(str(v))

        # Scheme check
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only http and https URLs are allowed")

        # Block localhost
        if parsed.hostname in {"localhost"}:
            raise ValueError("Localhost URLs are not allowed")

        # Block private IPs
        try:
            ip = socket.gethostbyname(parsed.hostname)
            if ipaddress.ip_address(ip).is_private:
                raise ValueError("Private IP addresses are not allowed")
        except Exception:
            pass  # DNS resolution may fail — don't hard block

        # Length check
        if len(str(v)) > 2048:
            raise ValueError("URL is too long")

        return v



