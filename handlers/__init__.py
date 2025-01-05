from aiogram import Router

from .other_handlers import router as router_1
from .user_handlers import router as router_2
from .wordly import router as router_3
from .calback import router as router_4
from .weather import router as router_5
from .book_handlers import router as router_6

router = Router()

router.include_router(router_6)
router.include_router(router_5)
router.include_router(router_4)
router.include_router(router_3)
router.include_router(router_2)
router.include_router(router_1)