FROM ubuntu
MAINTAINER Txivi

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# Install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    apt-utils \
    python3-pip \
    postgresql postgresql-contrib python3-dev \
    gcc libc-dev zlib1g zlib1g-dev libpq-dev \
    postgis
RUN pip3 install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./scripts /scripts

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
RUN chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

#USER user

CMD ["run.sh"]
