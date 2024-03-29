FROM python:3.9.16-slim-buster

ARG requirements_file
ARG dependencies

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1


RUN apt-get update -qq \
    && apt-get install -yq --no-install-recommends $dependencies \
    && pip install --upgrade pip
COPY ./$requirements_file .
RUN pip install -r $requirements_file

COPY . .

EXPOSE 8000

CMD python ./my_city/manage.py runserver 0.0.0.0:8000
