from .base import router as base_router
from .info import router as info_router
from .feedback import router as feedback_router
from .promo import router as promo_router
from .join import router as join_router  # ← добавляем

__all__ = [
    "base_router",
    "info_router",
    "feedback_router",
    "promo_router",
    "join_router",  # ← добавляем сюда тоже
]
