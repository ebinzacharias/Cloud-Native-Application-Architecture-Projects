import json
from concurrent import futures
from kafka import KafkaProducer
import grpc
import location_pb2
import location_pb2_grpc
import time

# Kafka configuration
KAFKA_HOST = "kafka"  # Kafka server host
KAFKA_PORT = "9092"      # Kafka server port
KAFKA_TOPIC = "location_topic"  # Kafka topic for location events

producer = KafkaProducer(
    bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# gRPC Setup
class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        # Location data from request
        location_data = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time
        }

        # Log the received location data
        print(f"Received location data: {location_data}")

        # Send the location data to Kafka
        producer.send(KAFKA_TOPIC, location_data)

        # Optionally: Print location data to verify it’s being sent
        print(f"Location event sent to Kafka: {location_data}")

        # Respond with an empty message (as per the .proto file)
        return location_pb2.Empty()


    def Get(self, request, context):
        # Logic for fetching location data from database (as per your requirements)
        pass

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

# Keep server alive
try:
    while True:
        time.sleep(86400)  # Sleep for a day, keep the service running
except KeyboardInterrupt:
    server.stop(0)

