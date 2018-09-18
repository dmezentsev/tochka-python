from datetime import datetime
from lxml import html

date_format = '%m/%d/%Y'


def get_content_ticker(body):
    """
    :param body: html document
    :return: xml-node table or []
    """
    tree = html.fromstring(body)
    table_content = tree.xpath('//div[@id = "historicalContainer"]//table')
    return table_content[0] if len(table_content) else []


def get_content_insider(body):
    """
    :param body: html document
    :return: xml-node table or []
    """
    tree = html.fromstring(body)
    table_content = tree.xpath('//table[@class = "certain-width"]')
    return table_content[0] if len(table_content) else []


def parse_table_ticker(table):
    """
    :param table: xml-node table
    :return: generator of dict in structure TickerLog
    """
    if not len(table):
        return
    table_columns = ['date', 'c_open', 'c_high', 'c_low', 'c_close', 'volume']
    for row in table.xpath('.//tbody/tr'):
        cells = [cell.strip() for cell in row.xpath('.//td//text()')]
        if len(cells) != len(table_columns):
            continue
        dist_cell = dict(zip(table_columns, cells))
        try:
            dist_cell['date'] = datetime.strptime(dist_cell['date'], date_format)
        except ValueError:
            continue
        dist_cell['volume'] = dist_cell['volume'].replace(',','')

        yield dist_cell


def parse_table_insider(table):
    """
    :param table: xml-node table
    :return: generator of dict in structure InsiderLog
    """
    if not len(table):
        return
    table_columns = ['name', 'relation', 'date', 'transaction_type', 'owner_type', 'shares_traded', 'last_price',
                     'shares_held']
    for row in table.xpath('./tr'):
        cells = [cell.strip() for cell in row.xpath('.//td//text()')]
        if len(cells) != len(table_columns):
            continue
        dist_cell = dict(zip(table_columns, cells))
        try:
            dist_cell['date'] = datetime.strptime(dist_cell['date'], date_format)
        except ValueError:
            continue
        dist_cell['shares_traded'] = dist_cell['shares_traded'].replace(',', '')
        dist_cell['shares_held'] = dist_cell['shares_held'].replace(',', '')

        yield dist_cell
