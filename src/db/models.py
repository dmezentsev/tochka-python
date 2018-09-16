from sqlalchemy import String, Text, BigInteger, Column, Date, ForeignKey, Integer, Boolean, Numeric, Index, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'

    id = Column(BigInteger, primary_key=True)
    code = Column(String(20))
    name = Column(String(255))

class TickerLog(Base):
    __tablename__ = 'ticker_log'

    id = Column(BigInteger, primary_key=True)
    company_id = Column(ForeignKey('company.id', ondelete=u'CASCADE'), nullable=False)
    company = relationship('Company')
    date = Column(Date)
    c_open = Column(Numeric(20,10))
    c_close = Column(Numeric(20,10))
    c_low = Column(Numeric(20,10))
    c_high = Column(Numeric(20,10))
    volume = Column(BigInteger)
