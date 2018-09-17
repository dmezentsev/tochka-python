from lxml import html, etree


def get_content_ticker(body):
    tree = html.fromstring(body)
    table_content = tree.xpath('//div[@class = "historicalContainer"]/table')
    print(table_content)
    return table_content


def is_correct_insider_log(body):
    return False


def get_ticker_log(body):
    yield []


def get_insider_log(body):
    yield []