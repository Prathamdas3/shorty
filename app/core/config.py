from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    env: str = Field(validation_alias="ENV")
    frontend_url: str = Field(validation_alias="FRONTEND_URL")
    debug: bool = Field(validation_alias="DEBUG")
    site_url: str = Field(validation_alias="SITE_URL", default="http://localhost:8080")
    og_image_url: str = Field(
        validation_alias="OG_IMAGE_URL", default="/static/icons/og_image.png"
    )
    social_github: str = Field(
        validation_alias="SOCIAL_GITHUB", default="https://github.com/"
    )
    social_twitter: str = Field(
        validation_alias="SOCIAL_TWITTER", default="https://twitter.com/"
    )
    social_linkedin: str = Field(
        validation_alias="SOCIAL_LINKEDIN", default="https://linkedin.com/in/"
    )
    site_description: str = Field(
        validation_alias="SITE_DESCRIPTION",
        default="Shorty is a free URL shortener with QR code generation. Shorten long URLs instantly and generate QR codes for easy sharing.",
    )
    site_keywords: str = Field(
        validation_alias="SITE_KEYWORDS",
        default="url shortener, qr code generator, link shortening, free url shortener, qr codes, url redirect",
    )


config = Config()
