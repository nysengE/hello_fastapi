from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    userid = ''
    passwd = ''
    dbname = ''
    dburl = ''
    sqlite_url = f'sqlite:///app/{dbname}.db'

config = Settings()