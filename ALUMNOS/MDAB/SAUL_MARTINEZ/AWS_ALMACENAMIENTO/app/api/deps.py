from app.core.config import get_settings
from app.db.session import get_session  # re-exportado para uso en routers
from app.services.storage import StorageService

__all__ = ["get_session", "get_storage"]


def get_storage() -> StorageService:
    return StorageService(get_settings())
