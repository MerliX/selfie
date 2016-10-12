[ ![Codeship Status for beevee/selfie_zmsh_2015](https://codeship.com/projects/7a3ec780-7d49-0132-04d9-42f9cc6659ff/status?branch=master)](https://codeship.com/projects/56612) [![Code Health](https://landscape.io/github/beevee/selfie_zmsh_2015/master/landscape.svg)](https://landscape.io/github/beevee/selfie_zmsh_2015/master)

Как запустить
=============

1. Установить питон 2.6 или 2.7
2. Установить peewee (должно сработать pip install peewee)
3. Установить Pillow (зависит от платформы, подробности в [документации](https://pillow.readthedocs.org/installation.html))
4. Прописать переменную окружения SELFIE_MODERATOR_CODE
5. Создать файл src/local_settings.py и переопределить в нем локальные пути (можно не делать, если стандартные пути подходят)
6. Создать таблицы в базе данных скриптом recreate_db.py. ОСТОРОЖНО: он удаляет существующие таблицы и создает новые пустые
7. По умолчанию приложение не раздает статические файлы. Лучше делать это через nginx. Пример конфигурации лежит в файле `nginx.conf.example`
8. Запустить python selfie.py. Демонизировать процесс можно с помощью supervisor, пример конфигурации лежит в файле `supervisor.ini.example`

How to run in Docker
====================

```
docker run -d -v selfie2:/data -p 80:80 merlix/selfie
```