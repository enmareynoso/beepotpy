from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.routes import honeypot_routes
    app.register_blueprint(honeypot_routes)
    return app
