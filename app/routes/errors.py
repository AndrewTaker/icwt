from flask import Response, jsonify
from http import HTTPStatus as status_code

def generic_error() -> tuple[Response, int]:
    return jsonify({
        "error": "Invalid data",
        "details": "Something went wrong"
    }), status_code.BAD_REQUEST.value

def validation_error(error: Exception) -> tuple[Response, int]:
    return jsonify({
        "error": "Invalid data",
        "details": str(error)
    }), status_code.BAD_REQUEST.value
