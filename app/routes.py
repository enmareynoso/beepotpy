from flask import Blueprint, request, jsonify
import logging

honeypot_routes = Blueprint("honeypot_routes", __name__)

logging.basicConfig(filename="logs/honeypot.logs", level=logging.INFO)

@honeypot_routes.route("/", methods=["GET", "POST"])
def honeypot():
    ip = request.remote_addr
    data = request.get_json if request.is_json else request.data.decode()

    logging.info(f"Attempt from {ip} with data: {data}")

    return jsonify({"message": "Access Denied"}), 403
                            