from collections import defaultdict, deque
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.generate_routes import generate_bp
from routes.history_routes import history_bp
from config import Config

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": Config.CORS_ORIGINS}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.register_blueprint(auth_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(history_bp)

_request_bucket = defaultdict(deque)


@app.before_request
def rate_limit():
    ip = request.remote_addr or "unknown"
    now = time.time()
    window_start = now - 60
    queue = _request_bucket[ip]
    while queue and queue[0] < window_start:
        queue.popleft()
    if len(queue) >= Config.RATE_LIMIT_PER_MINUTE:
        return jsonify({"error": "Too many requests"}), 429
    queue.append(now)


@app.errorhandler(Exception)
def unhandled_exception(error):
    print("UNHANDLED ERROR:", str(error))
    return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def home():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, threaded=True)