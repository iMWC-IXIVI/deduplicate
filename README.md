# Сервис, отвечающий за обнаружение дубликатов.

---
## Стек
### - Python:
- FastAPI
- Uvicorn
- Celery
- Clickhouse Driver
- Python-dotenv
- Redis
- MiniORM (Маленькая реализация ORM)
- Duplicate (Класс по определению дубликата)
### - Clickhouse
### - Redis
### - RabbitMQ
### - Celery-worker
### - Celery-beat (future)
### - Docker (docker compose)

---

## Настройка проекта

* __Клонирование проекта__ - ```git clone https://github.com/iMWC-IXIVI/deduplicate.git```
* __Необходимо перейти в директорию с проектом__ - ```cd deduplicate```
* __Копирование .env файла (необходимо настроить)__ - ```copy .env_example .env```
* __Создание необходимых папок для проекта__ - ```mkdir loggers celerybeat_data backups```
* __Создание виртуального окружения__ - ```python -m venv venv```
* __Активация виртуального окружения__ - ```venv/Scripts/activate```
* __Деактивация виртуального окружения (опционально)__ - ```deactivate```
* __Загрузка необходимых зависимостей__ - ```pip install -r req.txt```
* __Запуск docker compose (Система docker должна быть установлена)__ - ```docker compose up --build```
* __Просмотр файловой структуры docker'a (опционально)__ - ```docker exec -it <container_name> bash```
* __Исполнение команды docker сервиса (опционально)__ - ```docker exec -it <container_name> <command>```

___

## Эндпоинты

* __/service-event/ (POST)__ - Событие, на входе json с действием пользователя

___

## UserFlow

* __Пользователь отправляет запрос по эндпоинту /service-event/ (при нажатии на любую кнопку отпарвляются данные о действии).__
* __Ручка принимает данные и возвращает {"message": "ok"}, при любом случае, даже если запрос дублирующий.__
* __Данные, которые отправил пользователь перемещаются в стек задач (в RabbitMQ).__
* __После попадания задачи в стек, Celery-воркер забирает эту задачу и начинает проверять на дубликат.__
* __По итогу возвращает либо Success или Duplicate.__

___

## TODO
* [x] __Развёртывание сервисов в docker__
* [x] __Разработка своей ОРМ системы__
* [x] __Разработка системы миграций__
* [x] __Разработка задачи для celery-worker__
* [x] __Создание API "ручки"__
* [x] __Нагрузочное тестирование__
* [ ] __Работа с миграциями (Откат миграций - ATOMIC REQUESTS)__ - Атомарность относительна, добавляться не будет.
* [x] __Добавление celery-beat для выгрузки данных каждые 7 дней в файл, очистка бд каждые 7 дней__

---

## Как работает сервис?

---

Пользователь отправляет запрос в FastAPI сервис по паттерну http://localhost:8000/service-event/ (POST).

Пользователь вне зависимости от того, дублирующий ли запрос или нет получает ok, так как данные всё-таки аналитические, нет смысла прерывать пользователя.

Данные о его действии попадают в задачу deduplicate, с передаваемым аргументом data, где data данные пользователя о его действии.

Далее данные проверяются на сервисе redis, есть ли хэш данных в redis, если есть, значит дубликат, если нет, проверяем дальше.

После проверки на сервисе redis, идёт проверка в бд clickhouse, если есть хэш данных в бд, значит дубликат, если нет, далее сохраняем данные в redis, а именно хэш данных, а в бд сохраняем дату сохранения, uuid, сам хэш и данные.

Раз в 7 дней происходит резервное копирование данных, создаётся файл в папке backups с названием ГГ-ММ-ДД.log, а сама база данных чистится

Важный аспект TTL в бд не добавлялась, что бы исключить потерю данных во время резервного копирования.

На последних тестах сервер выдерживал 600 RPS.

Результат тестирования необходимо смотреть [тут](hard_test)