# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
# FROM python:3.7
# FROM python:3-buster
FROM ubuntu:bionic
# FROM debian:buster

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Thanks to https://github.com/phusion/baseimage-docker/issues/58
# ENV TERM=linux

# Set for all apt-get install, must be at the very beginning of the Dockerfile.
# Thanks to https://stackoverflow.com/questions/51023312/docker-having-issues-installing-apt-utils
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Tallinn

RUN apt-get update -y
# RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip

# create /src directory and copy required project source files to the image
RUN mkdir /src
# RUN echo 1; pwd ; ls -l
WORKDIR /src
# RUN echo 2; pwd ; ls -l
ADD setup.py .
ADD getlino getlino/
# RUN echo 3; pwd ; ls -l
RUN pip3 install -e .
#RUN pip3 install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

# Install sudo package and create a user lino
RUN apt-get install -y sudo
RUN adduser --disabled-password --gecos '' lino
RUN adduser lino sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER lino

RUN sudo -H getlino configure --batch --db-engine postgresql
RUN sudo -H getlino startsite --batch noi mysite1
