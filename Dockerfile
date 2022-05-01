FROM library/python:3.10-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get -y update
RUN apt-get -y install build-essential git python python-dev python-setuptools

COPY server/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY server/ /usr/src/app

EXPOSE 80

CMD ["sh", "./runserver.sh"]
