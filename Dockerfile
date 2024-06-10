FROM python:3.12-alpine
LABEL authors="romam"

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY .env /app/.env


COPY database/* /app/database/
COPY service/* /app/service/
COPY loader.py handlers.py settings.py main.py /app/


ENTRYPOINT ["python", "main.py"]

