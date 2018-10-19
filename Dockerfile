FROM python:3.6-slim

ENV REDIS_HOST 'redis'
ENV REDIS_PORT '6379'
ENV REDIS_DB '0'
ENV REDIS_PASSWORD ''

ENV APP_PORT '5000'
ENV APP_HOST '127.0.0.1'
ENV APP_SECRET 'abcd1234'
ENV APP_DEBUG 'false'

ENV URL_LOGOUT '/'
ENV URL_HOMEPAGE '/

ENV DISCORD_APPCODE '00000000'
ENV DISCORD_APICODE ''
ENV DISCORD_APISECRET ''
ENV DISCORD_REDIRECT '/'

WORKDIR /usr/src/app
COPY LoginHub ./LoginHub
COPY Config ./Config
COPY static ./static
COPY templates ./templates
COPY requirements.txt ./
COPY app.py ./

RUN pip install -r requirements.txt


EXPOSE 5000:5000/tcp

CMD ["python", "app.py"]