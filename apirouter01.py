from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.dbfactory import db_startup, db_shutdown


# 서버 시작시 디비 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_startup()
    yield
    await db_shutdown()

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    return 'Hello, APIRouter'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('apirouter01:app', reload=True)