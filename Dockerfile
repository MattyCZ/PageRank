FROM python:3.7-alpine
MAINTAINER chladond "chladond@fit.cvut.cz"
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache --update gcc musl-dev linux-headers libffi-dev openssl-dev g++ libxslt-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
