FROM ubuntu:14.04
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y python python-setuptools libpq-dev python-dev libjpeg-dev git-core python-psycopg2
RUN easy_install pip
RUN mkdir /opt/app
WORKDIR /opt/app
ADD requirements.txt /opt/app/
RUN pip install -r requirements.txt
ADD . /opt/app/
RUN echo "0 2 * * * /opt/app/shedule.sh" >> /etc/crontab
RUN chmod +x /opt/app/run.sh
CMD opt/app/run.sh