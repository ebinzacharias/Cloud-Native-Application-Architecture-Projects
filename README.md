# Project TechTrends

## Getting Started

### Prerequisites
Ensure the following tools are installed on your system:

- Python: 3.8.10
- Git: 2.25.1
- Docker: 28.0.0
- Vagrant: 2.4.0
- VirtualBox: 6.1.50_Ubuntur161033

You can fork or download the project from:
[https://github.com/udacity/nd064_course_1/tree/main/project](https://github.com/udacity/nd064_course_1/tree/main/project)


### Running the Application Locally

1. **Initialize the Database**
   
   Run the following command to create (or overwrite) the `database.db` file:
   ```bash
   python init_db.py
   ```

2. **Start the Flask Application**
   
   Run the application using:
   ```bash
   python app.py
   ```

   The application will be available at:
   [http://127.0.0.1:3111](http://127.0.0.1:3111)


## Best Practices for Application Deployment

### 1. Healthcheck Endpoint

As part of applying deployment best practices, a healthcheck endpoint `/healthz` was implemented. This allows systems like Kubernetes or load balancers to monitor the application’s availability.

### Objective
To implement a dedicated `/healthz` HTTP endpoint that returns a standardized health status for the Flask application.

### Endpoint Details
- **Route**: `/healthz`
- **Method**: `GET`
- **Response Code**: `200 OK`
- **Response Body**:
  ```json
  {
    "result": "OK - healthy"
  }
  ```

### Implementation
The `/healthz` endpoint was added to the Flask application in the `app.py` file as follows:

```python
@app.route('/healthz')
def healthz():
    return jsonify(result="OK - healthy"), 200
```

### Purpose and Importance of Healthchecks

In cloud-native systems, healthcheck endpoints play a critical role in ensuring application reliability and availability. Their primary function is to indicate whether an application is functioning properly and ready to serve requests.

Key use cases include:

- **Liveness Checks**: Confirm that the application process is running. If not, orchestrators like Kubernetes can automatically restart the container.
- **Readiness Checks**: Determine if the application is ready to receive traffic. This helps avoid sending requests to services that are not yet fully initialized.
- **Monitoring and Alerting**: Infrastructure monitoring tools can use these endpoints to track service health and notify teams of issues.
- **Load Balancer Health Routing**: Load balancers can route traffic only to healthy instances based on healthcheck results.

Even a simple check, like returning a 200 OK from a known endpoint, is enough to indicate that the application is alive. This check can later be extended to verify database connectivity, external service availability, or application-specific conditions.

### 2. Metrics Endpoint

As part of implementing observability best practices, a metrics endpoint `/metrics` was added. This endpoint provides basic runtime statistics that can be used for monitoring the application's activity and health over time.

### Objective
To implement a `/metrics` HTTP endpoint that returns real-time application metrics in JSON format. These metrics help in tracking how the application is being used and how often it interacts with the database.

### Endpoint Details
- **Route**: `/metrics`
- **Method**: `GET`
- **Response Code**: `200 OK`
- **Response Body** (example):
  ```json
  {
    "db_connection_count": 1,
    "post_count": 6
  }
  ```

### Implementation
The `/metrics` endpoint was added to the Flask application in the `app.py` file as follows:

```python
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    return jsonify(db_connection_count=db_connection_count, post_count=post_count), 200
```

Additionally, the `get_db_connection()` function was updated to increment a global `db_connection_count` variable every time a database connection is established:

```python
db_connection_count = 0

def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection
```

### Purpose and Importance of Metrics

Exposing application metrics is essential for understanding how an application is performing in real time. The metrics collected help identify performance bottlenecks, unusual activity, or trends in resource usage.
ng**: Helps anticipate scaling needs based on post volume and usage patterns.
- **Support for Observability**: Forms the foundation for deeper telemetry collection and analysis when combined with logs and traces.

The `/metrics` endpoint provides foundational insights into the application’s behavior without exposing sensitive or detailed information.
ies occur.
- **Capacity Planning**: Helps anticipate scaling needs based on post volume and usage patterns.
- **Support for Observability**: Forms the foundation for deeper telemetry collection and analysis when combined with logs and traces.

The `/metrics` endpoint provides foundational insights into the application’s behavior without exposing sensitive or detailed information.



### 3. Logging

To ensure traceability and enable debugging and observability, logging was added across key operations in the application. Logs are printed to STDOUT and include timestamps, log levels, and descriptive messages.

### Objective
To log important application events such as article retrieval, post creation, page access, and error cases. These logs help monitor usage patterns and troubleshoot issues efficiently.

### Implementation
Logging was configured using Python's built-in `logging` module. The configuration ensures all log messages are displayed on STDOUT with proper timestamps and at DEBUG level or higher:

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:app:%(asctime)s, %(message)s',
                    datefmt='%m/%d/%Y, %H:%M:%S')
```

### Events Logged
- **Article retrieved**:
  ```python
  logging.info(f'Article "{post["title"]}" retrieved!')
  ```

- **404 page shown**:
  ```python
  logging.info(f"Article ID {post_id} not found. Returning 404 page.")
  ```

- **About Us page accessed**:
  ```python
  logging.info("About Us page retrieved")
  ```

- **New article created**:
  ```python
  logging.info(f'New article "{title}" created!')
  ```

- **Missing title in form submission**:
  ```python
  logging.info('No Title is given')
  ```

### Example Log Output
```
INFO:app:04/11/2025, 18:45:10, Article "Cloud Native Architecture" retrieved!
INFO:app:04/11/2025, 18:45:12, About Us page retrieved
INFO:app:04/11/2025, 18:45:20, New article "Kubernetes 101" created!
```

### Purpose and Importance of Logging

- **Debugging**: Logs help developers understand the flow and identify issues.
- **Auditing**: Track who accessed what and when, especially useful in production environments.
- **Monitoring**: Logs provide real-time information for system health and behavior.
- **Incident Response**: During outages, logs are often the first source for root cause analysis.


## Docker for Application Packaging

The application was packaged using Docker for easier deployment and environment consistency. This allows the TechTrends project to be run in any environment that supports Docker.

### Objective
To write a Dockerfile, build an image, and run the Flask application inside a Docker container.

### Dockerfile Overview
A `Dockerfile` was created in the project root directory with the following steps:
- Uses `python:3.8-slim` as the base image
- Sets `/app` as the working directory
- Copies the application source files
- Installs dependencies from `requirements.txt`
- Initializes the database with `init_db.py`
- Exposes port `3111`
- Runs the application with `python app.py`

### Sample Dockerfile
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python init_db.py
EXPOSE 3111
CMD ["python", "app.py"]
```

### Building and Running the Image
The Docker image was built and tested locally:

```bash
# Build the image
docker build -t techtrends .

# Run the container in detached mode and map to host port 7111
docker run -d -p 7111:3111 techtrends
```

### Testing the Container
After running the container, the application was accessible at:
```
http://127.0.0.1:7111
```

All routes (`/`, `/create`, `/metrics`, `/about`) were tested successfully in the browser. A screenshot of the live application output was saved under `screenshots/docker-run-local.png`.

### Retrieving Logs
To view logs from the running container:

```bash
docker ps
docker logs <container_id>
```

Sample logs included standard Flask access logs and custom application logs, confirming that the containerized app works correctly and logs behave as expected.


