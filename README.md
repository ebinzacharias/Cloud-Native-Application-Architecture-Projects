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


## Continuous Integration with GitHub Actions

As part of automating the application packaging process, we implemented Continuous Integration (CI) using GitHub Actions. This ensures that every new push to the `main` branch results in a new Docker image being built and pushed to DockerHub.

### Objective
To automate the Docker image creation and publication process using GitHub Actions. This ensures faster iteration, consistency, and deployment readiness with every code change.

### GitHub Workflow File
A GitHub Actions workflow was created at:
```
.github/workflows/techtrends-dockerhub.yml
```

### Workflow Overview
- **Name**: TechTrends - Package with Docker
- **Trigger**: Every push to the `main` branch
- **Runner**: `ubuntu-latest`
- **Docker Tag**: `techtrends:latest`
- **Docker Registry**: DockerHub

### Workflow File Content
```yaml
name: TechTrends - Package with Docker

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./techtrends
          file: ./techtrends/Dockerfile
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/techtrends:latest
```

### Secrets Configuration
To avoid exposing sensitive information, the DockerHub credentials are securely stored using GitHub Secrets:
- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: DockerHub access token (generated in your DockerHub account)

Secrets were added in:
```
GitHub Repo → Settings → Secrets and variables → Actions
```

### Triggering the Workflow
After committing and pushing changes to the `main` branch, GitHub Actions is triggered. It builds and pushes the Docker image to DockerHub automatically.

### Verifying the Result
- **GitHub Actions**: A successful run of the workflow can be viewed under the **Actions** tab
- **DockerHub**: The new image with tag `latest` appears under the `techtrends` repository in the linked DockerHub account

### Screenshots
- `screenshots/ci-github-actions.png`: GitHub Actions successful workflow run
- `screenshots/ci-dockerhub.png`: DockerHub image listing with `techtrends:latest`

This integration ensures a reliable and repeatable packaging process for the TechTrends application every time new code is committed.


## Kubernetes Declarative Manifests

This section describes the process of deploying the TechTrends application on a Kubernetes cluster using declarative YAML manifests.

### Objective
To deploy the TechTrends application into a namespace `sandbox` using Kubernetes manifests for:
- Namespace
- Deployment
- Service

### Prerequisites
- Kubernetes cluster running with k3s (set up via Vagrant)
- kubectl configured and working inside the VM
- Docker image `ezachs/techtrends:latest` available on DockerHub

### YAML Manifests

#### namespace.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: sandbox
```

#### deploy.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: techtrends
  namespace: sandbox
spec:
  replicas: 1
  selector:
    matchLabels:
      app: techtrends
  template:
    metadata:
      labels:
        app: techtrends
    spec:
      containers:
      - name: techtrends
        image: ezachs/techtrends:latest
        ports:
        - containerPort: 3111
        resources:
          requests:
            cpu: 250m
            memory: 64Mi
          limits:
            cpu: 500m
            memory: 128Mi
        livenessProbe:
          httpGet:
            path: /healthz
            port: 3111
        readinessProbe:
          httpGet:
            path: /healthz
            port: 3111
```

#### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: techtrends
  namespace: sandbox
spec:
  selector:
    app: techtrends
  ports:
    - protocol: TCP
      port: 4111
      targetPort: 3111
  type: ClusterIP
```

### Apply Manifests
Run the following commands inside the VM:
```bash
kubectl apply -f namespace.yaml
kubectl apply -f deploy.yaml
kubectl apply -f service.yaml
```

### Verification
```bash
kubectl get all -n sandbox
```
Ensure that:
- A pod is running
- A deployment and replicaset exist
- A ClusterIP service is active

### Troubleshooting
- **ImagePullBackOff**: Ensure the Docker image exists and is public.
  Use `docker pull ezachs/techtrends:latest` to verify availability.
- **Namespace not found**: Apply `namespace.yaml` before other manifests.

### Screenshots to Include
- `screenshots/k8s-nodes.png`: Output of `kubectl get nodes`
- `screenshots/kubernetes-declarative-manifests.png`: Output of `kubectl get all -n sandbox`

This approach ensures your application is managed declaratively and is ready for production-like Kubernetes environments.




## Helm Chart for TechTrends

To make Kubernetes manifests reusable across environments, we converted them into a Helm Chart.

### Helm Chart Setup
Directory created:
```
helm/techtrends/
```

### Files Modified or Created
- `Chart.yaml`
- `values.yaml`
- `templates/namespace.yaml`
- `templates/deployment.yaml`
- `templates/service.yaml`

### Chart.yaml
```yaml
apiVersion: v2
name: techtrends
version: 1.0.0
keywords:
  - techtrends
maintainers:
  - name: ebin
```

### values.yaml (default)
```yaml
namespace: sandbox
image:
  repository: ezachs/techtrends
  tag: latest
  pullPolicy: IfNotPresent
service:
  port: 4111
  targetPort: 3111
  protocol: TCP
  type: ClusterIP
replicaCount: 1
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
containerPort: 3111
livenessProbe:
  path: /healthz
readinessProbe:
  path: /healthz
```

### Environment-specific Values
- `values-staging.yaml`
```yaml
namespace: staging
service:
  port: 5111
replicaCount: 3
resources:
  requests:
    memory: "90Mi"
    cpu: "300m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

- `values-prod.yaml`
```yaml
namespace: prod
service:
  port: 7111
image:
  pullPolicy: Always
replicaCount: 5
resources:
  requests:
    memory: "128Mi"
    cpu: "350m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

### Commands Used
Inside the VM:
```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm install techtrends-staging . -f values-staging.yaml --create-namespace
helm install techtrends-prod . -f values-prod.yaml --create-namespace
```

### Fix Applied
- Deleted `templates/NOTES.txt` to fix:
  ```
  Error: template: techtrends/templates/NOTES.txt:2:14: executing "...": nil pointer evaluating interface {}.enabled
  ```

### Verification
```bash
kubectl get all -n staging
kubectl get all -n prod
```
You should see deployments, services, and multiple running pods in each namespace based on the values provided.


## Continuous Delivery with ArgoCD

ArgoCD was used to implement continuous delivery of the TechTrends application to different environments using Helm.

### Objective
To automate and manage deployments using ArgoCD with Helm charts for the staging and production environments.

### ArgoCD Installation
- Installed in the Kubernetes cluster using the official install guide.
- Exposed ArgoCD server using a NodePort service.
- Verified pods using:
  ```bash
  kubectl get pods -n argocd
  ```
- Created the NodePort service:
  ```bash
  kubectl expose deployment argocd-server \
    --type=NodePort \
    --name=argocd-server-nodeport \
    --port=80 \
    --target-port=8080 \
    --namespace=argocd
  ```
- Verified external access:
  ```bash
  curl http://192.168.50.4:<NodePort>
  ```
  (e.g., NodePort: `31770`)

### ArgoCD Default Credentials
- **Username**: `admin`
- **Password**: Retrieved using:
  ```bash
  kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
  ```

### ArgoCD UI Access
- Accessible from host at: `http://192.168.50.4:<NodePort>` (e.g., `http://192.168.50.4:31770`)
- Screenshot saved as: `screenshots/argocd-ui.png`


## Continuous Delivery with ArgoCD

ArgoCD was used to deploy TechTrends to staging and production environments using Helm charts and automated synchronization.

### Objective
To set up ArgoCD on the Kubernetes (k3s) cluster and configure it to deploy TechTrends automatically via Helm with environment-specific values.

---

### ArgoCD Installation and Exposure

1. **Install ArgoCD in the k3s cluster:**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. **Expose the ArgoCD server using NodePort:**
```bash
kubectl expose deployment argocd-server \
  --type=NodePort \
  --name=argocd-server-nodeport \
  --port=80 \
  --target-port=8080 \
  --namespace=argocd
```

3. **Check the NodePort assigned:**
```bash
kubectl get svc argocd-server-nodeport -n argocd
```

Example output:
```
NAME                     TYPE       CLUSTER-IP       PORT(S)          NODE-PORT
argocd-server-nodeport   NodePort   10.43.185.253    80:31770/TCP     31770
```

4. **Access ArgoCD UI from the browser using VM IP:**
```
http://192.168.50.4:<nodePort>  # e.g., http://192.168.50.4:31770
```

---

### Access Credentials

1. **Get the default admin password:**
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

2. **Login as:**
- **Username:** `admin`
- **Password:** (output from above command)

---

### ArgoCD Applications (Manifests)

Two manifests were created in the `argo/` directory:
- `helm-techtrends-staging.yaml`
- `helm-techtrends-prod.yaml`

#### Sample structure of `helm-techtrends-prod.yaml`:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: techtrends-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: file:///home/vagrant/helm-chart
    targetRevision: HEAD
    path: .
    helm:
      valueFiles:
        - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

### File Upload to VM

1. Files were created in the host machine:
   - `argo/helm-techtrends-prod.yaml`
   - `argo/helm-techtrends-staging.yaml`

2. **Copied into the VM under `/home/vagrant/argo` using:**
```bash
vagrant upload ./techtrends/argo/helm-techtrends-prod.yaml /home/vagrant/argo
vagrant upload ./techtrends/argo/helm-techtrends-staging.yaml /home/vagrant/argo
```

3. **Verified inside VM:**
```bash
vagrant@localhost:~> ls /home/vagrant/argo
```

---

### Applying the Applications

```bash
kubectl apply -f /home/vagrant/argo/helm-techtrends-staging.yaml
kubectl apply -f /home/vagrant/argo/helm-techtrends-prod.yaml
```

---

### Troubleshooting

- **Problem:** ArgoCD UI not accessible
- **Reason:** NodePort not mapped correctly or ArgoCD pod restart
- **Solution:**
  - Deleted old service: `kubectl delete svc argocd-server-nodeport -n argocd`
  - Re-exposed the deployment using NodePort (as shown above)

- **Problem:** UI shows `failed to list refs: repository not found`
- **Reason:** Incorrect `repoURL` or not using an actual Git repo.
- **Solution:** Used local path with `repoURL: file:///home/vagrant/helm-chart` and verified file structure.

---

### Verification

- ArgoCD UI accessible at: `http://192.168.50.4:<nodePort>`
- Staging and Production apps synced and deployed
- Screenshots saved after successful sync:
  - `screenshots/argocd-techtrends-staging.png`
  - `screenshots/argocd-techtrends-prod.png`


