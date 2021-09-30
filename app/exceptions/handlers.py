from flask import Flask, json
from werkzeug.exceptions import HTTPException


def register_exception_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_bad_request(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    
    app.register_error_handler(400, handle_bad_request)