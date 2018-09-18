# tochka-python

## Общая информация

* Flask app. Usage: export FLASK_APP=src/web.py flask run
* CLI Loader. Usage: python src/loader.py -N 3 < tickers.txt

## Постановка
https://github.com/Life1over/test-task/blob/master/python.md

## Уточнения постановки:
Пункт 6 постановки. Разница всех атрибутов open/close/low/high на каждый день в интервале date_from - date_to 
относительно предыдущего дня

Пункт 7 постановки. Получить все уникальные непересекающиеся интервалы. 
Например, если исходный набор данных: `[100, 120, 110, 150, 160]`
* при `N=30`, результат: `[0:3]`.
* при `N=20`, результат: `[0:1], [1:3]`
* при `N=10`, результат: `[0:1], [1:2], [2:3], [3:4]`   