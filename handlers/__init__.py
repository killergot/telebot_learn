from aiogram import Router

from .other_handlers import router as router_1
from .user_handlers import router as router_2
from .wordly import router as router_3
from .photo_habdlers import router as router_photo
from .letter_handlers import router as router_letter
from .weather import router as router_5
from .book_handlers import router as router_6

router = Router()

router.include_router(router_photo)
router.include_router(router_letter)
router.include_router(router_6)
router.include_router(router_5)
router.include_router(router_3)
router.include_router(router_2)
router.include_router(router_1)