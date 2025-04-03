from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    try:
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "FAILED", "error": "exception"}), 500