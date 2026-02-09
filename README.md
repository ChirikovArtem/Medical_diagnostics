# Сайт медицинской организации
Это web-приложение на python написанное с использованием фреймворка Django, для стилизации используется Bootstrap.
Сайт сверстан и подключен к админке. Сайт содержит основные разделы, необходимые для записи на услугу и управления 
записями.

## Установка:
1. Клонируйте репозиторий:
```
https://github.com/ChirikovArtem/Medical_diagnostics
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Запуску проекта через docker-compose и проверка работоспособности

1. Установите Docker (для этого скачайте Docker Desktop с офицального сайта для вашей операционной системы: https://www.docker.com/products/docker-desktop.) 
2. Для запуска приложения введите команду в терминале: 
docker-compose up -d --build
3. После успешного запуска Django-приложение будет доступно по адресу http://localhost:8000

4. Для проверки запущенных контейнеров и их состояния введите команду:
 docker-compose ps

5. Для просмотра логов всех контейнеров (для отладки и мониторинга работы контейнеров) введите команду:
 docker-compose logs
6. 
## Функционал сайта:

### 1.Главная страница:
- Описание медицинской организации.
- Перечень предоставляемых услуг.
- Контактная информация.
- Форма для обратной связи.

### 2. Страница "О медицинской организации":
- История медицинской организации.
- Миссия и ценности.
- Команда.

### 3. Страница услуг: 
- Перечень предоставляемых медицинских услуг.
- Подробное описание каждой услуги.
- Цены на услуги.

### 4. Страница "Контакты": 
- Адрес компании.
- Карта проезда.
- Контактные телефоны и email.
- Форма обратной связи.

### 5."Личный кабинет":
- Регистрация и авторизация пользователей.
- Возможность записи на прием.
- Просмотр истории записей и результатов диагностики.

### 6. Админка:
- Управление пользователями.
- Управление услугами.
- Управление записями на прием.
- Управление контентом сайта (тексты, изображения и т.д.).

## Технические требования:

### 1.Фреймворк:
Использован фреймворк Django для реализации проекта.
### 2.База данных:
Используется PostgreSQL для хранения данных.
### 3.Фронтенд:
Использовался Bootstrap для создания адаптивного интерфейса.
### 4.Контейнеризация:
Использовать Docker и Docker Compose для контейнеризации приложения.
### 5.Качество кода:
Соблюдены стандарты PEP8.

## Модели реализованные в проекте:
### 1.User
Модель для регистрации, создания, обновления информации о пользователи.
Предусмотрена возможность смены пароля, при регистрации отправляется на почту письмо с подтверждением регистрации
### 2.Record
Модель для создания, редактирования, удаления записей на услуги
### 3.Registration
Модель для добавления, изменения, удаления информации о записи на услуги
### 4.Employee
Модуль для добавления, изменения, удаления информации о сотрудниках
### 5.Organisation
Модуль для изменения информации о медицинской организации
### 6.Покрытие кода тестами:
```
Name                                                Stmts   Miss  Cover
-----------------------------------------------------------------------
config\__init__.py                                      0      0   100%
config\asgi.py                                          4      4     0%
config\settings.py                                     36      0   100%
config\urls.py                                          7      0   100%
config\wsgi.py                                          4      4     0%
manage.py                                              11      2    82%
organisation\__init__.py                                0      0   100%
organisation\admin.py                                  17      0   100%
organisation\apps.py                                    3      0   100%
organisation\context_processors.py                      5      0   100%
organisation\forms.py                                  15      0   100%
organisation\migrations\0001_initial.py                 6      0   100%
organisation\migrations\__init__.py                     0      0   100%
organisation\models.py                                 38      1    97%
organisation\tests.py                                   0      0   100%
organisation\urls.py                                   10      1    90%
organisation\views.py                                 117     26    78%
registration\__init__.py                                0      0   100%
registration\admin.py                                   7      0   100%
registration\apps.py                                    3      0   100%
registration\forms.py                                  37      8    78%
registration\migrations\0001_initial.py                 7      0   100%
registration\migrations\__init__.py                     0      0   100%
registration\models.py                                 13      0   100%
registration\services.py                               20      1    95%
registration\tests.py                                  94     18    81%
registration\urls.py                                    6      0   100%
registration\views.py                                  86     40    53%
users\__init__.py                                       0      0   100%
users\admin.py                                          5      0   100%
users\apps.py                                           3      0   100%
users\forms.py                                         41      1    98%
users\management\__init__.py                            0      0   100%
users\management\commands\__init__.py                   0      0   100%
users\management\commands\create_admin_group.py        20     20     0%
users\management\commands\create_manager_group.py      45     45     0%
users\management\commands\csu.py                       10     10     0%
users\managers.py                                      14      1    93%
users\migrations\0001_initial.py                        8      0   100%
users\migrations\0002_alter_user_number_snils.py        4      0   100%
users\migrations\0003_alter_user_managers.py            4      0   100%
users\migrations\__init__.py                            0      0   100%
users\models.py                                        21      0   100%
users\tests.py                                         43      0   100%
users\urls.py                                          10      1    90%
users\views.py                                         58      4    93%
-----------------------------------------------------------------------
TOTAL                                                 832    187    78%
```