from fastapi import APIRouter
from api.routes import price_router, ui_router, upload_router

router = APIRouter()
router.include_router(ui_router, tags=["ui"], prefix="/ui")
router.include_router(price_router, tags=["price"], prefix="/price")
router.include_router(upload_router, tags=["upload"], prefix="/upload")
