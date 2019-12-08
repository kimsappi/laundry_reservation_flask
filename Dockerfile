FROM python:3-alpine

LABEL version="0.0.1"

RUN pip3 install flask sqlalchemy

COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
