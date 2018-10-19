FROM python:3.6-slim

ENV REDIS_HOST ''
ENV REDIS_PORT ''
ENV REDIS_DB ''
ENV REDIS_PASSWORD ''

ENV APP_PORT ''
ENV APP_HOST ''
ENV APP_SECRET ''
ENV APP_DEBUG ''
ENV APP_LOGOUT ''
ENV APP_HOMEPAGE ''

ENV URL_DISCORD ''

WORKDIR /usr/src/app
COPY LoginHub ./
COPY Config ./
COPY requirements.txt ./
COPY app.py ./

RUN pip install -r requirements.txt


EXPOSE 5000:5000/tcp

CMD ["python", "app.py"]