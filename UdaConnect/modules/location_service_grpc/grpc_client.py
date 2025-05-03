import grpc
import location_pb2
import location_pb2_grpc

# Internal gRPC client setup for the Location Service
channel = grpc.insecure_channel('localhost:5006')  # Update with the correct service name
stub = location_pb2_grpc.LocationServiceStub(channel)

# Example Create Location request
response = stub.Create(location_pb2.LocationMessage(person_id=1, longitude=40.7128, latitude=-74.0060, creation_time="2022-08-01"))
print("Response from Location Service:", response)

