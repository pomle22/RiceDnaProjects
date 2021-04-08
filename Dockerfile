FROM python:3.7-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /app
COPY ./src/requirements.txt /app

# Install required package
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    ca-certificates gcc python3-dev musl-dev postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    git bash \
    && apk add --no-cache mariadb-dev

RUN pip install mysqlclient  


# Install requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./src/ /app
WORKDIR /app

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

