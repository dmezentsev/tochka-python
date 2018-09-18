import configparser
from contextlib import contextmanager
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_orm_session(url):
    """
    :param url: SQLAlchemy connection url
    :return: sessionmaker
    """
    engine = create_engine(url, encoding='utf-8')
    return sessionmaker(bind=engine, autocommit=True)


@contextmanager
def get_orm_session(session):
    """
    :param session: SQLAlchemy sessionmaker
    :return: SQLAlchemy session
    """
    s = session()
    yield s
    s.close()


def get_db_url(config_path):
    """
    Config adapter to SQLAlchemy
    :param config_path: config file in directory __config__
    :return: str
    """
    dirname = os.path.dirname(__file__)
    cp = configparser.ConfigParser()
    cp.read('{}/__config__/{}'.format(dirname, config_path))
    db_config = cp['default']
    return '{protocol}://{user}:{password}@{host}:{port}/{dbname}'.format(
        protocol=db_config.get('protocol', 'postgresql'),
        user=db_config.get('user', 'postgres'),
        password=db_config.get('password', ''),
        host=db_config.get('host', 'localhost'),
        port=int(db_config.get('port', 5432)),
        dbname=db_config.get('dbname', 'postgres')
    )
