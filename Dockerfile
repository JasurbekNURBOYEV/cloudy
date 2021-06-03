FROM python:3.8

RUN mkdir /cloudy
WORKDIR /cloudy
COPY requirements.txt /cloudy/
RUN pip install -r requirements.txt
COPY . /cloudy/