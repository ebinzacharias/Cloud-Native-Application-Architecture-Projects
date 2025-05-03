import json
from kafka import KafkaConsumer
import os
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'location_topic')

# Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',
    group_id='connection-service-group'
)

# Function to process Kafka messages
def process_kafka_messages():
    for message in consumer:
        # Deserialize the message
        location_event = json.loads(message.value.decode('utf-8'))

        # Here, you can process the event, like storing it in a DB or taking some action
        logger.info(f"Received location event: {location_event}")
        
        # Example: Call a function to save the location event to a database
        # save_to_db(location_event)

# Start Kafka Consumer in a separate thread
def start_kafka_consumer():
    consumer_thread = threading.Thread(target=process_kafka_messages)
    consumer_thread.daemon = True  # Daemonize the thread so it terminates with the main process
    consumer_thread.start()

# Start consuming Kafka messages when the app starts
start_kafka_consumer()
