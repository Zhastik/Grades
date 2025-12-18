from fastapi import FastAPI

from app.db import connect_pool, close_pool
from app.routers import router as routers

app = FastAPI(title="Grades API")

@app.on_event("startup")
async def startup():
    await connect_pool()

@app.on_event("shutdown")
async def shutdown():
    await close_pool()

app.include_router(routers)
