from http import HTTPStatus as status_code

from flask import Response, jsonify


def generic_error(e: Exception = ValueError("qq")) -> tuple[Response, int]:
    return jsonify({
        "error": "Invalid data",
        "details": "Something went wrong",
        "debug_err": str(e),
    }), status_code.BAD_REQUEST.value


def validation_error(error: Exception) -> tuple[Response, int]:
    return jsonify({
        "error": "Invalid data",
        "details": str(error)
    }), status_code.BAD_REQUEST.value


def date_range_error(start_date: str, end_date: str) -> tuple[Response, int]:
    return jsonify({
        "error": "Invalid date range",
        "details": f"Start_date must be earlier than end_date {start_date=} {end_date=}"
    }), status_code.BAD_REQUEST.value
