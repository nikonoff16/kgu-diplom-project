# Бекэнд универсальной платформы запуска контейнеризированных приложений

## Тестовая среда

### Первый (холодный) запуск

1. Клонируем репозиторий `git clone git@github.com:nikonoff16/kgu-diplom-project.git`
2. Переходим в папку с сервисом `cd backend`
3. Создаем файл `.dev.env` в этой директории, наполняем его содержимым (см. раздел в конце данного руководства). 
4. Настраиваем переменные окружения в файле `.dev.env` (он используется по умолчанию)
5. Делаем миграции для создания базы данных `docker-compose run web python manage.py makemigrations` и `docker-compose run web python manage.py migrate`
6. Создаем суперпользователя: `docker-compose run web python manage.py makesuperuser` и сохраняем пароль, который появится в консоли. 
7. Запускаем локальный сервер `docker-compose up`
8. По адресу `http://localhost:8060/admin` будет доступна консоль администратора. Авторизоваться по почте и паролю из шага 6. 
9. Посмотреть документацию к интерфейсам можно по адресу `http://localhost:8060/swagger-ui/`

### Повторные запуски

1. Не забываем перейти в папку с сервисом: `cd backend`
2. Делаем миграции для создания базы данных `docker-compose run web python manage.py makemigrations` и `docker-compose run web python manage.py migrate`
3. Запускаем локальный сервер `docker-compose up`
4. По адресу `http://localhost:8060/admin` будет доступна консоль администратора. Авторизоваться по почте и паролю, которые должны быть сохранены из этапа холодного запуска (см. выше). 
5. Изучаем документацию к интерфейсам по адресу `http://localhost:8060/swagger-ui/`

## Продуктовая среда
Принцип запуска не отличается от того, что можно найти в руководстве по тестовому запуску, но для нормальной работы необходимо выполнить следующие шаги:
1. В файле конфигурации `red/backend/config/settings.py` необходимо определиться с хостами, с которых разрешено вызывать сервис;
2. Создаем в папке `red/backend` файл `.env`, наполняем его содержимым (см. раздел в конце данного руководства); 
3. Правим информацию в файле из предыдущего шага - добавляем информацию о продуктовых сервисах (БД и прочих), и убеждаемся, что переменная `DEBUG` установлена в `False`; 
4. В `red/backend/docker-compose.yaml` необходимо указать продуктовый файл с переменными из предыдущего шага в поле `env_file`. 
5. Далее, как уже сказано, выполнить шаги из соответствущего блока тестового запуска.

## Файл переменных окружения
Для теста и для прода имеются разные файлы окружения. Это необходимо для корректной разработки и безопасности продовой среды.
Ниже привожу все обязательные переменные, которые должны в нем присутствовать:
```angular2html
DATABASE_URL=postgresql://db_url:5432/db_name
DATABASE_NAME=db_name
DATABASE_USER=db_user
DATABASE_PASSWORD=some_password
DATABASE_HOST=some_host_url.ru
DATABASE_PORT=5432
REDIS_URL=redis://some_redis_url:6679/0
DJANGO_SECRET_KEY=123
DJANGO_DEBUG=True
```# kgu-diplom-project