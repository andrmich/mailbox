FROM python:3.8-buster

RUN mkdir /mailbox
RUN mkdir /supervisor

WORKDIR /code

RUN apt-get update
RUN apt-get install -y supervisor
RUN apt-get install -y nginx nginx-extras apache2-utils python3-fusepy


COPY requirements.txt .
RUN pip install -r requirements.txt
COPY code/ .

COPY webdav.conf /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/sites-enabled/*

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord"]


