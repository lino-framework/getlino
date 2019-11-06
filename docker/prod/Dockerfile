ARG DEBIAN_FRONTEND=noninteractive
FROM debian:buster
#FROM https://cloud.docker.com/repository/docker/khchine5/debian_latest
#FROM khchine5:debian_latest
ENV TERM=linux
ENV PYTHONUNBUFFERED=1
RUN sudo mkdir /src
# RUN echo 1; pwd ; ls -l
WORKDIR /src
# RUN echo 2; pwd ; ls -l
#ADD . src/
ADD setup.py .
ADD getlino getlino/
RUN sudo chown lino:lino -R /src
# RUN echo 3; pwd ; ls -l src
RUN sudo pip3 install -e .
#RUN pip3 install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

# USER lino
# RUN sudo -H getlino configure --batch --db-engine postgresql  && sudo -H getlino startsite --batch noi mysite1 --dev-repos "lino noi xl"
