from contextlib import contextmanager


class BufferProcessor:
    """
        Buffer access
        Supports parallel processes
    """
    def __init__(self, orm_session, session_id=None):
        self.orm_session = orm_session
        self.session_id = session_id or self.start_import_session()

    def start_import_session(self):
        return self.orm_session.execute('select nextval(:sequence)', {'sequence': 'session_id'}).scalar()

    def load_buffer(self, model, ticker, data):
        for row in data:
            row['session_id'] = self.session_id
            row['ticker'] = ticker
            self.orm_session.execute(model.__table__.insert(), row)

    def normalize_buffer(self):
        self.orm_session.execute('''
            insert into company (code) 
                select ticker 
                    from 
                        ticker_buffer tb
                            left join
                        company t on t.code = tb.ticker
                    where
                        tb.session_id = :session_id and
                        t.id is null
                    group by tb.ticker;
    
            insert into ticker_log (company_id, date, c_open, c_close, c_low, c_high, volume)
                select t.id, tb.date, tb.c_open, tb.c_close, tb.c_low, tb.c_high, tb.volume
                    from 
                        ticker_buffer tb
                            join
                        company t on t.code = tb.ticker
                            left join
                        ticker_log tl on 
                            tl.company_id = t.id and
                            tl.date = tb.date
                    where 
                        tb.session_id = :session_id and
                        tl.id is null;
    
            insert into insider (company_id, name, relation)
                select t.id, ib.name, max(ib.relation)
                    from
                        insider_buffer ib
                            join
                        company t on t.code = ib.ticker
                            left join
                        insider i on
                            i.name = ib.name and
                            i.company_id = t.id
                    where
                        ib.session_id = :session_id and
                        i.id is null
                    group by t.id, ib.name;
    
            insert into insider_log (insider_id, date, transaction_type, owner_type, 
                                     shares_traded, last_price, shares_held)
                select  i.id, ib.date, ib.transaction_type, max(ib.owner_type), 
                        max(ib.shares_traded), max(ib.last_price), max(ib.shares_held)
                    from
                        insider_buffer ib
                            join
                        company t on t.code = ib.ticker
                            join
                        insider i on 
                                i.name = ib.name and
                                i.company_id = t.id
                            left join
                        insider_log il on
                                il.insider_id = i.id and
                                il.date = ib.date and
                                il.transaction_type = ib.transaction_type
                    where
                        ib.session_id = :session_id and
                        il.id is null
                    group by i.id, ib.date, ib.transaction_type;
            ''', {'session_id': self.session_id})

    def close_import_session(self):
        """
        Clear buffer temporary data
        """
        for table in ['ticker_buffer', 'insider_buffer']:
            self.orm_session.execute('delete from {} where session_id = :session_id'.format(table),
                                     {'session_id': self.session_id})


@contextmanager
def processing_buffer(orm_session, session_id=None):
    buffer = BufferProcessor(orm_session, session_id)
    yield buffer
    buffer.normalize_buffer()
    buffer.close_import_session()