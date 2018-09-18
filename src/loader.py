import argparse
import asyncio
import aiohttp
import sys

from db.connector import create_orm_session, get_orm_session, get_db_url
from parser import get_content_ticker, get_content_insider, parse_table_ticker, parse_table_insider
from db.load import processing_buffer
from db.models import TickerBuffer, InsiderBuffer


async def worker(pid, http_session, queue):
    """
    :param pid: worker number
    :param http_session: aiohttp session
    :param queue: list of tasks
    :return:
    """
    while len(queue):
        ticker, type, page, get_content, get_data = queue.pop()
        print('PID: {}, ticker: {}, page: {}'. format(pid, ticker, page))
        path = 'insider-trades?page={}'.format(page) if type is InsiderBuffer else 'historical'
        async with http_session.get('http://www.nasdaq.com/symbol/{}/{}'.format(ticker, path)) as response:
            data = await response.text()
        print('DONE: PID: {}, ticker: {}, page: {}'. format(pid, ticker, page))
        content = get_content(data)
        if len(content) and page < 10:
            # First 10 pages. Send next task if current request success
            queue.append([ticker, InsiderBuffer, page + 1, get_content_insider, parse_table_insider])
        buffer.load_buffer(type, ticker, get_data(content))  # load data in denormalized buffer


async def asynchronous(workers, queue):
    """
    :param workers: count workers
    :param queue: list of Tickers e.q. ['GOOG', 'AAPL', 'CVX']
    :return:
    """
    task = []
    for t in queue:         # create task for workers
        if not t.strip():
            continue
        task.append([t.strip(), TickerBuffer, 0, get_content_ticker, parse_table_ticker])
    async with aiohttp.ClientSession() as http_session:
        tasks = [asyncio.ensure_future(worker(i, http_session, task)) for i in range(workers)]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    tickers = sys.stdin                 # read Tickers from stdin

    parser = argparse.ArgumentParser(description='Load data from Nasdaq')
    parser.add_argument('-N', metavar='N', type=int, help='workers count')
    args = parser.parse_args()
    workers_count = args.N              # read count workers from cli

    session = create_orm_session(get_db_url('db.conf'))
    with get_orm_session(session) as orm, processing_buffer(orm) as buffer:  # use buffer
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(asynchronous(workers_count, tickers))
        ioloop.close()
