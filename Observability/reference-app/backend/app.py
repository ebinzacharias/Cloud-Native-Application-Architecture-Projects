from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_pymongo import PyMongo
from jaeger_client import Config
from flask_opentracing import FlaskTracing
import atexit

app = Flask(__name__)
metrics = PrometheusMetrics(app, path='/metrics')

# MongoDB config
app.config["MONGO_DBNAME"] = "example-mongodb"
app.config["MONGO_URI"] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"
mongo = PyMongo(app)

# Tracer setup using Jaeger Agent (UDP on port 6831)
def init_tracer(service_name='backend'):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'logging': True,
            'reporter_batch_size': 1,
            'local_agent': {
                'reporting_host': 'jaeger-agent.observability.svc.cluster.local',
                'reporting_port': 6831
            }
        },
        service_name=service_name,
        validate=True
    )
    return config.initialize_tracer()

# Initialize tracer
tracer = init_tracer()
atexit.register(tracer.close)
tracing = FlaskTracing(tracer, True, app)

# Root route
@app.route("/")
def homepage():
    with tracer.start_span("homepage") as span:
        span.set_tag("message", "Hello World")
        return "Hello World"

# /api route
@app.route("/api")
def my_api():
    with tracer.start_span("api-span") as span:
        span.set_tag("endpoint", "/api")
        return jsonify(response="something")

# /star route
@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span("star-span") as span:
        try:
            star = mongo.db.stars
            name = request.json["name"]
            distance = request.json["distance"]
            star_id = star.insert({"name": name, "distance": distance})
            new_star = star.find_one({"_id": star_id})
            output = {"name": new_star["name"], "distance": new_star["distance"]}
            span.set_tag("status", "success")
            return jsonify({"result": output})
        except Exception as e:
            span.set_tag("error", True)
            span.log_kv({'event': 'error', 'error.object': str(e)})
            return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()

