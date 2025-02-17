# scrapy_tehpst
Асинхронный парсер основанный на фреймворке Scrapy собирает данные товаров с сайта tehpst.site. Собираем полную информацию по товарам (название, описание, артикул, цена, остатки на складах, характеристики товаров).

## Особенности:
– Группы и классы товаров парсим в файлы в json формате. Далее ссылки на товары и каждый товар, включающий полную информацию, парсим с сохранением в базу данных MySQL.
- Предполагается, что у вас развернута база MySQL локально или удаленно. Для локально развернутой базы используйте ветку "master", для удаленной "one_full_item".
- В варианте удаленной базы scrapy возвращает Item-объект, содержащий полную информацию о товаре. Это несколько снижает асинхронность, но значительно снижает количество запросов к БД. При этом парсер работает быстрее.

## Запуск проекта локально
Для запуска проекта выполните следующие шаги:

Склонируйте репозиторий scrapy_tehpst на свой компьютер.
'''bash git clone 
'''
Создайте и активируйте виртуальное окружение:
для Windows
python -m venv venv
source venv/Scripts/activate
для Linux/macOS
python3 -m venv venv
source venv/bin/activate
Обновите pip:
для Windows
python -m pip install --upgrade pip
для Linux/macOS
python3 -m pip install --upgrade pip
Установите зависимости из файла requirements.txt:
pip install -r requirements.txt
Создайте и заполните файл .env на примере env.example.
Запустите подряд несколько пауков: 
scrapy crawl tehpst_group -O groups.json
scrapy crawl tehpst_class -O classes.json
scrapy crawl tehpst_products
scrapy crawl tehpst_full_products

Автор:
Александр Русанов, shurik.82rusanov@yandex.ru
