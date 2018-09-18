from flask import Flask, render_template, url_for, request
from db.models import Company, TickerLog, Insider, InsiderLog
from db.connector import create_orm_session, get_orm_session, get_db_url
from sqlalchemy import and_, text
import json

app = Flask(__name__)
session = create_orm_session(get_db_url('db.conf'))


def api_wrapper(rule, **options):
    """API call support"""
    def wrapper(f):
        app.route(rule, **options)(f)
        app.route('/api' + rule, **options)(f)
        return f
    return wrapper


def is_api_call():
    """Choose JSON/HTML strategy"""
    if request.path.startswith('/api/'):
        return True
    return False


@api_wrapper("/")
def tickers():
    with get_orm_session(session) as orm:
        tcks = [ticker.strip() for ticker, in orm.query(Company.code).all()]
        if is_api_call():
            return json.dumps(tcks)
        return render_template('list.tpl',
                               data=[(ticker, url_for('ticker_log', ticker=ticker)) for ticker in tcks])


@api_wrapper("/<ticker>")
def ticker_log(ticker):
    with get_orm_session(session) as orm:
        logs = orm.query(TickerLog).join(Company).filter(and_(Company.code == ticker, TickerLog.date >= text(
            """current_date - interval '3 month'"""))).order_by(TickerLog.date.desc()).all()
        if is_api_call():
            data = []
            for log in logs:
                data.append({'date': log.date, 'c_open': log.c_open, 'c_close': log.c_close, 'c_low': log.c_low,
                             'c_high': log.c_high})
            return json.dumps(data)
        return render_template('ticker_log.tpl', data=logs)


@api_wrapper("/<ticker>/insider")
def insider(ticker):
    with get_orm_session(session) as orm:
        insiders = [insdr.strip() for insdr, in
                    orm.query(Insider.name).join(Company).filter(Company.code == ticker).order_by(Insider.name).all()]
        if is_api_call():
            return json.dumps(insiders)
        return render_template('list.tpl',
                               data=[(insdr, url_for('insider_log', ticker=ticker, insdr=insdr)) for insdr in insiders])


@api_wrapper("/<ticker>/insider/<insdr>")
def insider_log(ticker, insdr):
    with get_orm_session(session) as orm:
        logs = orm.query(InsiderLog).join(Insider).join(Company).filter(and_(Company.code == ticker, Insider.name == insdr)).order_by(
            InsiderLog.date.desc()).all()
        if is_api_call():
            data = []
            for log in logs:
                data.append({'date': log.date, 'transaction_type': log.transaction_type, 'owner_type': log.owner_type,
                             'shares_traded': log.shares_traded, 'last_price': log.last_price,
                             'shares_held': log.shares_held})
            return json.dumps(data)
        return render_template('insider_log.tpl', data=logs)


@api_wrapper("/<ticker>/analytics")
def report_analytics(ticker):
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    with get_orm_session(session) as orm:
        logs = orm.query(TickerLog).join(Company).filter(
            and_(Company.code == ticker, TickerLog.date.between(date_from, date_to))).order_by(TickerLog.date).all()
        data = []
        prev_log = None
        for log in logs:
            prev_log = prev_log or log
            data.append(
                {'date': log.date, 'c_open': log.c_open - prev_log.c_open, 'c_close': log.c_close - prev_log.c_close,
                 'c_low': log.c_low - prev_log.c_low, 'c_high': log.c_high - prev_log.c_high})
            prev_log = log
        if is_api_call():
            return json.dumps(data)
        return render_template('ticker_log.tpl', data=data)


@api_wrapper("/<ticker>/delta")
def report_delta(ticker):
    delta = request.args.get('value')
    metric = request.args.get('type')
    binds = {'open': 'c_open', 'high': 'c_high', 'low': 'c_low', 'close': 'c_close'}
    if metric not in binds:
        return 'FAILED TYPE: {}'.format(metric)
    with get_orm_session(session) as orm:
        logs = orm.execute("""
        with log_interval as (select  -- log_interval: all intervals with delta over `:delta`
            tl.date,
            min(tl_t.date) as todate
          from
            company c
              join
            ticker_log tl on
                tl.company_id = c.id
              join
            ticker_log tl_t on
                tl_t.company_id = tl.company_id and
                tl_t.date > tl.date and
                abs(tl_t.{metric} - tl.{metric}) > :delta
          where
            c.code = :ticker
          group by tl.date)
          select li.date, li.todate
            from
              log_interval li
                left join
              log_interval li_f on    -- FILTER: only earliest and unique intervals
                  li_f.date < li.date and
                  li.todate between li_f.date and li_f.todate
            where li_f.date is null
            order by li.date
        """.format(metric=binds[metric]), {'ticker': ticker, 'delta': delta})
        data = []
        for log in logs:
            data.append(
                {'date': log.date, 'todate': log.todate})
        if is_api_call():
            return json.dumps(data)
        return render_template('rep_delta.tpl', data=data)