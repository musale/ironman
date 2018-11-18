FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["./entrypoint.sh"]
