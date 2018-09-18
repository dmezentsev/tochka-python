from flask import Flask, render_template, url_for, request
from db.models import Company, TickerLog, Insider, InsiderLog
from db.connector import create_orm_session, get_orm_session, get_db_url
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
    """JSON vs HTML strategy"""
    if request.path.startswith('/api/'):
        return True
    return False


def orm_result(objects, extractor):
    for obj in objects:
        yield extractor(obj)


@api_wrapper("/")
def tickers():
    with get_orm_session(session) as orm:
        tcks = [ticker.strip() for ticker, in orm.query(Company.code).all()]
        if is_api_call():
            return json.dumps(tcks)
        return render_template('list.tpl',
                               data=[(ticker.strip(), url_for('ticker_log', name=ticker)) for ticker, in tcks])


@api_wrapper("/<name>")
def ticker_log(name):
    with get_orm_session(session) as orm:
        ticker_log = orm.query(TickerLog).filter(Company.code == name).order_by(TickerLog.date.desc()).all()
        return renderer('ticker_log.tpl', data=orm_result(ticker_log))


@api_wrapper("/<name>/insider")
def insider(name):
    with get_orm_session(session) as orm:
        insiders = orm.query(Insider.name).filter(Company.code == name).order_by(Insider.name).all()
        return renderer('list.tpl', data=[insider.strip() for insider, in insiders])
