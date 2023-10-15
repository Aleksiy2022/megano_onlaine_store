FROM python:3.10.5

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY megano /megano
COPY diploma-frontend /diploma-frontend

RUN cd /diploma-frontend && python setup.py sdist
RUN cd /diploma-frontend/dist && pip install diploma-frontend-0.6.tar.gz
