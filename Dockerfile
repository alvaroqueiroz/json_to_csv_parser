FROM python:3

WORKDIR /usr/src/app

COPY datafile1.json ./
COPY datafile2.json ./
COPY out_expected.csv ./

RUN pip install pytest

COPY . .

RUN pytest