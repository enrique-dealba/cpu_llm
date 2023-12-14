from flask import jsonify


def handle_exceptions(func):
    """Decorator to handle exceptions in Flask routes."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
    return wrapper
