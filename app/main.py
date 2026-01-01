from fastapi import FastAPI
from .core.logging import get_logger
from .routers.api.v1 import product_router, author_router, user_router, auth_router
app = FastAPI()
logger = get_logger()

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")

app.include_router(router=product_router.router)
app.include_router(router=author_router.router)
app.include_router(router=user_router.router)
app.include_router(router=auth_router.router)
