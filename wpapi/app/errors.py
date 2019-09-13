from flask import make_response, jsonify


def page_not_found(e):
    response = make_response(
        jsonify({"error_code": 404, "message": str(e.description)})
    )
    response.status_code = 404
    return response
