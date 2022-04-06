# syntax=docker/dockerfile:1

FROM python:3.10.3-slim-buster

WORKDIR /app

COPY Pipfile Pipfile
RUN pip3 install pipenv
RUN pipenv install

COPY . .

CMD ["python3", "-m", "app.main", "--host=0.0.0.0"]