from sqlalchemy import String, Text, BigInteger, Column, Date, ForeignKey, Integer, Boolean, Numeric, Index, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'

    id = Column(BigInteger, primary_key=True)
    code = Column(String(20))
    ticker_log = relationship('TickerLog')
    insider = relationship('Insider')


class TickerLog(Base):
    __tablename__ = 'ticker_log'

    id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey('company.id'))
    date = Column(Date)
    c_open = Column(Numeric(20,10))
    c_close = Column(Numeric(20,10))
    c_low = Column(Numeric(20,10))
    c_high = Column(Numeric(20,10))
    volume = Column(BigInteger)


class Insider(Base):
    __tablename__ = 'insider'

    id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey('company.id'))
    name = Column(String(255))
    relation = Column(String(50))
    insider_log = relationship('InsiderLog')


class InsiderLog(Base):
    __tablename__ = 'insider_log'

    id = Column(BigInteger, primary_key=True)
    insider_id = Column(BigInteger, ForeignKey('insider.id'))
    date = Column(Date)
    transaction_type = Column(String(50))
    owner_type = Column(String(50))
    shares_traded = Column(BigInteger)
    last_price = Column(Numeric(20,10))
    shares_held = Column(BigInteger)


class TickerBuffer(Base):
    __tablename__ = 'ticker_buffer'

    id = Column(BigInteger, primary_key=True)
    session_id = Column(BigInteger)
    ticker = Column(String(20))
    date = Column(Date)
    c_open = Column(Numeric(20, 10))
    c_close = Column(Numeric(20, 10))
    c_low = Column(Numeric(20, 10))
    c_high = Column(Numeric(20, 10))
    volume = Column(BigInteger)


class InsiderBuffer(Base):
    __tablename__ = 'insider_buffer'

    id = Column(BigInteger, primary_key=True)
    session_id = Column(BigInteger)
    ticker = Column(String(20))
    name = Column(String(255))
    relation = Column(String(50))
    date = Column(Date)
    transaction_type = Column(String(50))
    owner_type = Column(String(50))
    shares_traded = Column(BigInteger)
    last_price = Column(Numeric(20,10))
    shares_held = Column(BigInteger)