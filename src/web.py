from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Company

app = Flask(__name__)


def api_wrapper(rule, **options):
    def wrapper(f):
        app.route(rule, **options)(f)
        app.route('/api' + rule, **options)(f)
        return f
    return wrapper


def render_wrapper(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)


@api_wrapper("/")
def tickers():
    orm_engine = create_engine('postgresql://postgres:1@127.0.0.1:5432/ticker', encoding='utf-8')
    session = sessionmaker(bind=orm_engine, autocommit=True)
    tickers = session().query(Company.code).all()
    session.close_all()
    return render_template('list.tpl', data=[(ticker.strip(), url_for('ticker_log', name=ticker.strip())) for ticker, in tickers])


@api_wrapper("/<name>")
def ticker_log(name):
    return render_template('table.tpl', data=[[123] * 8] * 3)
