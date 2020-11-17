FROM python:3.8-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /alice3data

WORKDIR /alice3data
RUN pip3 install -e .