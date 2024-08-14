from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.dbfactory import db_startup, db_shutdown
from app.routes.member_router import member_router
from app.routes.sungjuk_router import sungjuk_router


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

app.include_router(member_router, prefix='/member')
app.include_router(sungjuk_router, prefix='/sungjuk')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('apirouter01:app', reload=True)
