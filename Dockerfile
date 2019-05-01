FROM python:latest

RUN apt-get update && apt-get install -yq vim curl gettext
RUN mkdir /root/hardwar
COPY . /root/hardwar
WORKDIR /root/hardwar
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

