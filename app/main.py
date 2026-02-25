from fastapi import FastAPI
from .core.logging import get_logger
from .routers.api.v1 import product_router, author_router, user_router, auth_router, cart_router
app = FastAPI()
logger = get_logger()
from app.core.redis import connect_redis, close_redis

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")
    
@app.on_event("startup")
async def startup():
    await connect_redis()
    
    
@app.on_event("shutdown")
async def shutdown():
    await close_redis()

app.include_router(router=product_router.router)
app.include_router(router=author_router.router)
app.include_router(router=user_router.router)
app.include_router(router=auth_router.router)
app.include_router(router=cart_router.router)