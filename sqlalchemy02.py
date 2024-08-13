# 회원정보를 이용한 CRUD
# mno, userid, passwd, name, email, regdate
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing_extensions import Optional

sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url,
                       connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# 데이터 베이스 모델 정의
Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'

    mno = Column(Integer, primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime)

# 데이터 베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal() # 데이터베이스 세션 객체 생성
    try:
        yield db    # yield : 파이썬 제너레이터 객체
        # 함수가 호출될 때 객체를 반환 (넘김)
    finally:
        db.close()  # 데이터베이스 세션 닫음 (디비 연결해체,리소스 반환)

class MemberModel(BaseModel):
    mno: int
    userid: str
    passwd: str
    name: str
    email: str
    regdate : datetime

app = FastAPI()

@app.get('/')
def index():
    return 'Hello, World!!'

# 맴버 조회
# Depends : 의존성 주입 - db 세션 제공
# => 코드 재사용성 향상, 관리 용이성 향성
@app.get('/mem', response_model=List[MemberModel])
def read_mem(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 멤버 상세 조회 - 멤버번호로 조회
@app.get('/mem/{mno}', response_model=Optional[MemberModel])
def readone_mem(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member

# 멤버 추가
@app.post('/mem', response_model=MemberModel)
def memadd(mem: MemberModel, db: Session = Depends(get_db)):
    mem = Member(**dict(mem))    # 클라이언트가 전송한 멤버 데이터가
    # pydantic으로 유효성 검사 후
    # 데이터베이스에 저장할 수 있도록
    # sqlalchemy 객체로 변환

    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem

@app.put('/mem', response_model=Optional[MemberModel])
def update_mem(mem: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mem.mno).first()
    if member:
        for key, val in mem.dict().items():
            setattr(member, key, val)
            db.commit()
            db.refresh(member)
    return member

# 멤버 삭제 - 멤버번호로 조회
# 먼저, 삭제할 멤버 데이터가 있는지 확인한 후 삭제 실행
@app.delete('/mem', response_model=Optional[MemberModel])
def readone_mem(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member:
        db.delete(member)
        db.commit()
    return member
# __name__: 실행중인 모듈 이름을 의미하는 매직키워드
# 만일, 파일을 직접 실행 하면 __name__의 이름은 __name__으로 자동 지정
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)