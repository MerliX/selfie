FROM python:2.7

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get update && apt-get install -y nginx

# Change me
ENV http_host=localhost
ENV SELFIE_MODERATOR_CODE=123456

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN echo "upstream selfie {\n\
    server 127.0.0.1:8080 fail_timeout=0;\n\
}\n\
\n\
server {\n\
    listen       80;\n\
    server_name  $http_host;\n\
\n\
    client_max_body_size  5M;\n\
    keepalive_timeout     5;\n\

    location /static/ {\n\
        root  /selfie/;\n\
    }\n\
\n\
    location /selfies/ {\n\
        root  /selfies/;\n\
    }\n\
\n\
    location ~ ^/(favicon|apple-touch-icon|mstile|browserconfig).*\.(png|ico|xml)$ {\n\
        root /selfie/static/favicons/;\n\
    }\n\
\n\
    location / {\n\
        proxy_set_header Host       $http_host;\n\
        proxy_redirect         off;\n\
        proxy_connect_timeout  15;\n\
        proxy_read_timeout     15;\n\
        proxy_pass             http://selfie;\n\
    }\n\
}\n"\
> /etc/nginx/conf.d/default.conf

COPY ./ /selfie/

RUN echo "PHOTO_PATH = '/data/selfies/'\n\
DB_PATH = '/data/base.db'\n\
DEBUG = False\n\
SELFIE_REWARD = 10\n"\
>> /selfie/src/local_settings.py

EXPOSE 80
WORKDIR /selfie/
ENTRYPOINT ["bash", "docker.sh"]