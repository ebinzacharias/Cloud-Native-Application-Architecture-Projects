import grpc
import location_pb2
import location_pb2_grpc

# Create a channel and a stub for gRPC communication
channel = grpc.insecure_channel('localhost:5005')  # Location Service gRPC server
stub = location_pb2_grpc.LocationServiceStub(channel)

# Send a location creation request
location = location_pb2.LocationMessage(
    person_id=5,
    longitude=-76.23489283,
    latitude=832.86789,
    creation_time='2021-08-30',
)

response = stub.Create(location)  # gRPC call to create the location
print("Response from Location Service:", response)

