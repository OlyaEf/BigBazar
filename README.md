
<p align="center">
  <img src="images/visual.png" alt="BigBazar Interface"/>
</p>

# BigBazar Backend API

Этот проект - API для сервиса покупки товаров, реализованный на Python и использующий PostgreSQL в качестве базы данных. Сервис предоставляет возможности регистрации и авторизации пользователей, а также управление товарным каталогом и корзиной покупок.

## Оглавление

- [Настройка и запуск](#настройка-и-запуск)
- [Примеры использования](#примеры-использования)
- [Тесты](#тесты)
- [Лицензия](#лицензия)

## Настройка и запуск

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/OlyaEf/BigBazar.git
    ```

2. Установите зависимости командой: 

    ```bash
    poetry install
    poetry shell
    ```

3. Настройте файл `.env` на основе `.env_example` и создайте базу данных

    ```sql
    CREATE DATABASE bigbazar_db;
    ```

4. Выполните миграции

    ```bash
    aerich init -t bb.core.config.TORTOISE_ORM
    aerich init-db
    aerich migrate
    aerich upgrade
    ```
Инициализация Aerich: aerich init -t bb.core.config.TORTOISE_ORM
Создает необходимые таблицы в базе данных на основе определенных моделей данных: aerich init-db
Создание миграции: aerich migrate
Применение миграции: aerich upgrade
Применение изменений, если есть: aerich upgrade


5. Запустите сервер

    ```bash
    uvicorn bb.main:app --reload 
    ```

## Примеры использования

* Документация API доступна по адресам:
  * http://localhost:8000/docs
  * http://localhost:8000/redoc

 **Методы для всех пользователей:**

  * Регистрация
  * Авторизация

 **Методы для авторизованных пользователей:**

  * Управление товарами (создание, чтение, обновление, удаление)
  * Просмотр списка пагинированных товаров

## Тесты

Для запуска тестов:

1. Запустите тесты:

    ```bash
    coverage run -m pytest
    ```

2. Просмотрите отчет о покрытии:

    ```bash
    coverage report
    ```

## Лицензия

* (c) 2023 @OlyaEf - [Лицензия](docs/LICENSE.md)

[Смотреть презентацию BigBazar](docs/BigBazar_prezentation.pdf)
