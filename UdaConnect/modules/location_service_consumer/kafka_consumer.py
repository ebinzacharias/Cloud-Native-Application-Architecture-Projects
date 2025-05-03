from kafka import KafkaConsumer
import json
import grpc
import location_service_pb2
import location_service_pb2_grpc
import logging

logging.basicConfig(level=logging.INFO)

# Kafka Consumer configuration
consumer = KafkaConsumer(
    'location-events',  # Kafka topic
    bootstrap_servers=['localhost:9093'],  # Kafka broker
    group_id='location-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def start_kafka_consumer():
    for message in consumer:
        logging.info(f"Received message: {message.value}")
        # Process the incoming Kafka message (location data)
        person_id = message.value.get('person_id')
        longitude = message.value.get('longitude')
        latitude = message.value.get('latitude')
        creation_time = message.value.get('creation_time')

        # Call the gRPC service to store the location data
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = location_service_pb2_grpc.LocationServiceStub(channel)
            location_message = location_service_pb2.LocationMessage(
                person_id=person_id,
                longitude=longitude,
                latitude=latitude,
                creation_time=creation_time
            )
            stub.Create(location_message)
            logging.info(f"Location for person {person_id} created successfully.")

if __name__ == "__main__":
    start_kafka_consumer()

