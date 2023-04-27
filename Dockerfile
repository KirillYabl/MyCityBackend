FROM python:3.9.16-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./dev-requirements.txt .
RUN pip install -r dev-requirements.txt

COPY . .

EXPOSE 8000

CMD python ./my_city/manage.py runserver 0.0.0.0:8000
