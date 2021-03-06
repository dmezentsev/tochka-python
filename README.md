# tochka-python

## Общая информация

* Flask app. Usage: export FLASK_APP=src/web.py flask run
* CLI Loader. Usage: python src/loader.py -N 3 < tickers.txt

## Требования к серверу

* `python >= 3.6`
* `postgresql >= 9.5`

## Deploy

* `pip install -r requirements.txt`
* `psql < sql/init.sql` (создание DB и пользователя)
* `psql -U ticker_user -p < sql/structure.sql` (важно выполнить из-под пользователя ticker_user)
* `edit src/db/__config__/db.conf` (настройки подключения к базе) 

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

## Комментарии
Какие есть нюансы реализации, которые могут зависеть от конкретной специфики использования инструмента?

1. Можно использовать инструмент синхронизации структуры БД на основе моделей `SQLAlchemy`. Из известных мне: `alembic`.
Однако в таком подходе необходимо более полное описание самих моделей. И в данном случае речь не идет о постоянных
патчах хранилища. По моему мнению, структура достаточно стабильна.
2. Менеджмент подключений к postgres отдан на откуп внешнего инструментария. Для PG достаточно критично иметь пулл 
соединений. Релизация может быть различной: на стороне приложения или, например, при помощи готового инструмента 
`pgbouncer`.
3. Обработка задач получения данных с портала `nasdaq` реализована в концепции минимизации количества запросов. Поэтому 
для малого количества ticker-ов может работать не совсем оптимально. Например, если указали 10 потоков при 3 задачах, 
работать будет реально только 3, потому что запросы происходят последовательно с целью получения информации, о наличии
данных. Если нет информации по самому ticker-у, то запросы по insider-ам не уйдут. Аналогично, если нет информации на
5-ой странице по insider-ам, на 6-ую страницу запросы не отправятся. Здесь надо понимать, чем жертвуем трафиком или 
скоростью
4. Помимо aiohttp можно использовать aiopg для импорта данных. Однако, в данном случае в связи с небольшими объемами и
наличием буффера для данных, вставка должна происходить достаточно быстро, думаю, экономия будет незначительной
