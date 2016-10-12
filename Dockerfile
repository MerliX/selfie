FROM python:2.7

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get update && apt-get install -y nginx

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ./ /selfie/

RUN echo "PHOTO_PATH = '/data/selfies/'\n\
SQLITE_DB_PATH = '/data/base.db'\n\
DEBUG = False\n\
USE_POSTGRES = False\n\
SELFIE_REWARD = 10\n"\
>> /selfie/src/local_settings.py

EXPOSE 80
WORKDIR /selfie/
COPY ./selfies/unknown.jpg /data/selfies/unknown.jpg
ENTRYPOINT ["bash", "docker.sh"]