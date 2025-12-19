from fastapi import FastAPI
from .core.logging import get_logger

app = FastAPI()
logger = get_logger()

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")

@app.get('/')
def root():
    # logger.info("this is test logger")
    return {"hello book store api project"}