from unittest.mock import MagicMock

from app.core.config import Settings
from app.services.storage import StorageService


def _settings() -> Settings:
    return Settings(
        s3_bucket_name="mi-bucket",
        aws_region="eu-west-1",
        s3_presign_expiration=900,
    )


def test_presigned_get_url_uses_get_object():
    client = MagicMock()
    client.generate_presigned_url.return_value = "https://s3/get"
    service = StorageService(_settings(), client=client)

    url = service.presigned_get_url("productos/1/foto.jpg")

    assert url == "https://s3/get"
    client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={"Bucket": "mi-bucket", "Key": "productos/1/foto.jpg"},
        ExpiresIn=900,
    )


def test_presigned_put_url_includes_content_type():
    client = MagicMock()
    client.generate_presigned_url.return_value = "https://s3/put"
    service = StorageService(_settings(), client=client)

    url = service.presigned_put_url("productos/1/foto.jpg", "image/png")

    assert url == "https://s3/put"
    client.generate_presigned_url.assert_called_once_with(
        "put_object",
        Params={
            "Bucket": "mi-bucket",
            "Key": "productos/1/foto.jpg",
            "ContentType": "image/png",
        },
        ExpiresIn=900,
    )
