import uvicorn

from fastapi import FastAPI

from api import router


app = FastAPI(
    title='Event',
    version='1.0.0'
)
app.include_router(router=router)
