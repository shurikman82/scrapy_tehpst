# scrapy_tehpst
Асинхронный парсер основанный на фреймворке Scrapy собирает данные товаров с сайта tehpst.site. Собираем полную информацию по товарам (название, описание, артикул, цена, остатки на складах, характеристики товаров).

## Особенности:
- Группы и классы товаров парсим в файлы в json формате. Далее ссылки на товары и каждый товар, включающий полную информацию, парсим с сохранением в базу данных MySQL.
- Предполагается, что у вас развернута база MySQL локально или удаленно. Для локально развернутой базы используйте ветку "master", для удаленной "one_full_item".
- В варианте удаленной базы scrapy возвращает Item-объект, содержащий полную информацию о товаре. Это несколько снижает асинхронность, но значительно снижает количество запросов к БД. При этом парсер работает быстрее.

## Запуск проекта локально
Для запуска проекта выполните следующие шаги:

Склонируйте репозиторий scrapy_tehpst на свой компьютер.
```bash
git clone git@github.com:shurikman82/scrapy_tehpst.git
```
Создайте и активируйте виртуальное окружение:
для Windows
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
для Linux/macOS
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
Обновите pip:
для Windows
```bash
python -m pip install --upgrade pip
```
для Linux/macOS
```bash
python3 -m pip install --upgrade pip
```
Установите зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Создайте и заполните файл .env на примере env.example.
Запустите подряд несколько пауков:
```bash
scrapy crawl tehpst_group -O groups.json
```
```bash
scrapy crawl tehpst_class -O classes.json
```
```bash
scrapy crawl tehpst_products
```
```bash
scrapy crawl tehpst_full_products
```

Автор:
Александр Русанов, shurik.82rusanov@yandex.ru
