FROM python:3.9-alpine

# Install dependencies for Kafka consumer, Postgres, etc.
RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port for Flask REST API
EXPOSE 5000

# Copy application code into the container
COPY . .

# Start the Flask app and the Kafka consumer
CMD ["sh", "-c", "python app/udaconnect/kafka_consumer.py & flask run --host=0.0.0.0"]
