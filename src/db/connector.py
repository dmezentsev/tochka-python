from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_orm_session(url):
    engine = create_engine(url, encoding='utf-8')
    return sessionmaker(bind=engine, autocommit=True)


@contextmanager
def get_orm_session(session):
    s = session()
    yield s
    s.close()