import argparse
import asyncio
import aiohttp
import sys

from parser import get_content_ticker, get_ticker_log, is_correct_insider_log, get_insider_log

tickers = []
for ticker in sys.stdin:
    tickers.append([ticker.strip(), 'ticker', 0, get_content_ticker, get_ticker_log])


parser = argparse.ArgumentParser(description='Load data from Nasdaq')
parser.add_argument('-N', metavar='N', type=int, help='workers count')
args = parser.parse_args()
workers_count = args.N


async def worker(pid, session):
    while len(tickers):
        ticker, type, page, get_content, get_data = tickers.pop()
        print('PID: {}, ticker: {}'. format(pid, ticker))
        path = 'insider-trades?page={}'.format(page) if type == 'insider' else 'historical'
        async with session.get('http://www.nasdaq.com/symbol/{}/{}'.format(ticker, path)) as response:
            data = await response.text()
        print('DONE: PID: {}, ticker: {}, dt: {}'. format(pid, ticker, data))
        if get_content(data):
            tickers.append([ticker, 'insider', page + 1, is_correct_insider_log, get_insider_log])


async def asynchronous():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(worker(i, session)) for i in range(workers_count)]
        await asyncio.wait(tasks)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
