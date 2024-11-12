from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from api import router as router_v1



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)