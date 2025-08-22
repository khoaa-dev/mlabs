from flask import Flask, jsonify
from flask_cors import CORS
from .db import db, DATABASE_URL
from .models import Contact, Message  
from .router.contacts import router as contacts_router
from .router.messages import router as messages_router

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure CORS
    CORS(app, origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
    ])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(contacts_router)
    app.register_blueprint(messages_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(400)
    def bad_request(e): return jsonify(error="bad_request"), 400

    @app.errorhandler(404)
    def not_found(e): return jsonify(error="not_found"), 404

    @app.errorhandler(500)
    def internal(e): return jsonify(error="internal_error"), 500

    return app

app = create_app()

if __name__ == "__main__":
    # In Docker, expose port 5143
    app.run(host="0.0.0.0", port=5143)
