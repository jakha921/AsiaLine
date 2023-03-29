FROM python:3.10.9

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
