import time

from flask import Flask, jsonify

from app.routes.tasks import tasks_bp

_start_time = time.time()


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "uptime": time.time() - _start_time})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
