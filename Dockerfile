FROM python:3.12-alpine
LABEL authors="romam"

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

