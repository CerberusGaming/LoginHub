FROM python:3.6-slim

ENV REDIS_HOST 'redis'
ENV REDIS_PORT '6379'
ENV REDIS_DB '0'
ENV REDIS_PASSWORD ''

ENV APP_PORT '5000'
ENV APP_HOST '127.0.0.1'
ENV APP_SECRET 'abcd1234'
ENV APP_DEBUG 'false'
ENV APP_LOGOUT '/logout'
ENV APP_HOMEPAGE '/home'

ENV URL_DISCORD '/'

WORKDIR /usr/src/app
COPY LoginHub ./
COPY Config ./
COPY requirements.txt ./
COPY app.py ./

RUN pip install -r requirements.txt


EXPOSE 5000:5000/tcp

CMD ["python", "app.py"]