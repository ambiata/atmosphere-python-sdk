from typing import Dict

import flask
from pydantic import ValidationError


class BaseTransformer:
    """
    Basic implementation of SeldonComponent to link with our
    custom activity and handle the boilerplate transformation methods
    that we need..
    """

    # https://docs.seldon.io/projects/seldon-core/en/v1.1.0/python/python_component.html#user-defined-exceptions
    model_error_handler = flask.Blueprint("error_handlers", __name__)

    @staticmethod
    @model_error_handler.app_errorhandler(ValidationError)
    def handle_custom_error(validation_error):
        response = flask.jsonify(validation_error.errors())
        response.status_code = 422
        return response

    def tags(self) -> Dict:
        return {}
