from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

# 회원정보를 이용한 CRUD
# userid, passwd, name, email, regdate

class Member(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

member_db: List[Member] = []

app = FastAPI()

@app.get('/')
def index():
    return 'Hello, pydantic!! - Member'

@app.get('/member', response_model=List[Member])
def member():
    return member_db

@app.post('/member', response_model=Member)
def memberok(m: Member):
    member_db.append(m)
    return m

@app.get('/member/{userid}', response_model=Member)
def memberok(userid: str):
    # regdate 값을 문자열 대신 datetime 객체로 생성
    memberone = Member(userid='none', passwd='none', name='none',
                       email='none', regdate=datetime(1970, 1, 1, 0, 0, 0))
    for m in member_db:
        if m.userid == userid:
            memberone = m
    return memberone

@app.delete('/member/{userid}', response_model=Member)
def memberdel(userid: str):
    # regdate 값을 문자열 대신 datetime 객체로 생성
    memberone = Member(userid='none', passwd='none', name='none',
                       email='none', regdate=datetime(1970, 1, 1, 0, 0, 0))
    for idx, m in enumerate(member_db):
        if m.userid == userid:
            memberone = member_db.pop(idx)
    return memberone

@app.put('/member', response_model=Member)
def membermod(one: Member):
    # regdate 값을 문자열 대신 datetime 객체로 생성
    putone = Member(userid='none', passwd='none', name='none',
                    email='none', regdate=datetime(1970, 1, 1, 0, 0, 0))
    for idx, m in enumerate(member_db):
        if m.userid == one.userid:
            member_db[idx] = one
            putone = one
    return putone

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('pydantic02:app', reload=True)
