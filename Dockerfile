FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

WORKDIR $APP_HOME

RUN apt-get -y update \
    && apt-get install -y build-essential libpq-dev libffi-dev python3-dev libssl-dev vim gcc \
    && apt-get -y clean

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt --no-cache-dir

ADD . /app

EXPOSE 8010

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
