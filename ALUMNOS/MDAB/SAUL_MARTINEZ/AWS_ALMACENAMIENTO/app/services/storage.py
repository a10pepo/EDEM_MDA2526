"""Servicio de almacenamiento en S3 con URLs prefirmadas.

El bucket es privado: nunca se sirven objetos públicamente. Para mostrar una
imagen del catálogo se genera una URL prefirmada de lectura (GET) temporal, y
para subir una imagen, una URL prefirmada de escritura (PUT).
"""

import boto3

from app.core.config import Settings


class StorageService:
    def __init__(self, settings: Settings, client=None):
        self._settings = settings
        self._bucket = settings.s3_bucket_name
        self._expiration = settings.s3_presign_expiration
        # Si no se inyecta cliente, se construye con la config (en AWS las
        # credenciales vienen del IAM Instance Role => sin claves en el código).
        self._client = client or boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def presigned_get_url(self, key: str) -> str:
        """URL temporal para LEER (servir) un objeto del catálogo."""
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=self._expiration,
        )

    def presigned_put_url(self, key: str, content_type: str = "image/jpeg") -> str:
        """URL temporal para SUBIR un objeto (el cliente hace PUT directo a S3)."""
        return self._client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self._bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=self._expiration,
        )
