from fastapi import FastAPI
from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from app.dbfactory import engine

sqlite_url = 'sqlite:///app/clouds2024.db'
engine = create_engine(sqlite_url, connect_args={}, echo=True)
app = FastAPI()

# SQLAlchemy Base 설정
Base = declarative_base()

class Zipcode(Base):  # SQLAlchemy 모델로 Zipcode 정의
    __tablename__ = 'zipcode'

    zipcode = Column(Integer, index=True)
    sido = Column(String)
    gugun = Column(String)
    dong = Column(String)
    ri = Column(String)
    bunji = Column(String)
    seq = Column(String, primary_key=True)

@app.get('/')
def index():
    return 'Hello, Jinja2!!'

@app.get('/zipcode/{dong}')
def zipcode(dong: str):
    result = ''

    with Session(engine) as sess:
        stmt = select(Zipcode).where(Zipcode.dong.like(f'{dong}'))
        rows = sess.scalars(stmt)

        for row in rows:
            result += f'{row.zipcode} {row.sido} {row.gugun} {row.dong}'

    return f'{result}'

@app.get('/sido')
def getsido():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('jinja01:app', reload=True)
