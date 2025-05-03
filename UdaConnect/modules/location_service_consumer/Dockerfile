FROM python:3.8-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers g++ postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .

CMD ["python", "kafka_consumer.py"]

