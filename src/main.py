from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.routes.v1 import router_v1


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
