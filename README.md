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

### Healthcheck Endpoint

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


