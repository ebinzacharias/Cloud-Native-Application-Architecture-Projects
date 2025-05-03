# Task 1: 1. Review and Plan
1. Review the starter project [starter project](https://github.com/udacity/cd0309-message-passing-projects-starter)
2. Determine which message passing strategies would integrate well when refactoring to a microservice architecture.


# Task 1: Review and Plan

## Planned Refactored Microservices

The monolith will be broken into the following services:

1. **Person Service**
2. **Location Service**
3. **Connection Service**
4. **API Gateway** (new component)
5. **Kafka Broker** (new component)

## Message Passing Strategy for Refactoring UdaConnect

### 1. **gRPC** – Internal Communication Between Core Microservices

* **Use Case**: Location Ingestion Service ⇌ Person Service
* **Justification**: gRPC is chosen for its high performance, low latency, and compact binary data format using Protocol Buffers. Ideal for internal service-to-service communication, especially under heavy location data ingestion.

---

### 2. **Kafka** – Event Streaming from Location Service

* **Use Case**: Location Service ⇨ Kafka ⇨ Connection Service
* **Justification**: Kafka enables asynchronous, scalable processing of high-throughput location events. The pub-sub model decouples services and supports fault-tolerant ingestion pipelines.

---

### 3. **REST** – External and Frontend-Facing Communication

* **Use Case**: Frontend ⇌ API Gateway ⇌ Microservices
* **Justification**: REST is a widely adopted, human-readable protocol perfect for external interaction. It supports frontend access and CRUD operations with minimal learning curve.

---


