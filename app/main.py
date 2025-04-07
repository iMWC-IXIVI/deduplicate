import uvicorn

from fastapi import FastAPI

from api import router


app = FastAPI(
    title='Deduplicate',
    version='1.0.0'
)
app.include_router(router=router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
