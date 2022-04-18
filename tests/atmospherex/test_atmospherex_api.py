import json
import os
from sys import getdefaultencoding
from typing import Optional

import jwt
import requests_mock

from atmosphere.atmospherex import AtmospherexAPI
from atmosphere.atmospherex.atmospherex_auth import AuthSettings

atmospherex_base_url = "http://atmospherex.base-url.com"
activity_endpoint = "conversation-rate-optimisation"


def get_match_request_auth_method(auth_settings: Optional[AuthSettings]):
    def the_matcher_method(request):
        # Without auth settings, just validate that the client did not send any
        # auth headers.
        if auth_settings is None:
            if "authorization" in request.headers:
                raise ValueError(
                    "The header authorisation should not have been populated by"
                    " the atmosphere client api."
                )
            return True

        # With auth headers, validate that the token is valid
        if "authorization" not in request.headers:
            raise ValueError(
                "The header authorisation should be populated by the atmosphere"
                " client api."
            )

        auth_header = request.headers.get("authorization")
        if not auth_header.lower().startswith("bearer "):
            raise ValueError("The authorization should be a bearer token")
        token_str = auth_header[7:]
        jwt.decode(
            token_str,
            audience=auth_settings.jwt_audience,
            algorithms=auth_settings.jwt_sign_algorithm,
            key=auth_settings.jwt_secret.get_secret_value(),
        )
        return True

    return the_matcher_method


def mock_prediction_requests(mock_request, auth_settings: Optional[AuthSettings]):
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data/count",
        status_code=200,
        json={"count": 150},
        additional_matcher=get_match_request_auth_method(auth_settings),
    )
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data",
        status_code=200,
        json={
            "predictions": [{"user": "James", "order": "spicy meatball sandwich"}] * 100
        },
        additional_matcher=get_match_request_auth_method(auth_settings),
    )
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data?skip=100",
        status_code=200,
        json={
            "predictions": [{"user": "Jim", "order": "spicy meatball sandwich"}] * 50
        },
        additional_matcher=get_match_request_auth_method(auth_settings),
    )


def test_atmospherex_count():
    for auth_settings in [None, AuthSettings("me", "me_subject", "secret")]:
        api = AtmospherexAPI(atmospherex_base_url, auth_settings)

        with requests_mock.Mocker(real_http=True) as mock_request:
            mock_request.register_uri(
                "GET",
                f"{atmospherex_base_url}/api"
                f"/inferences/{activity_endpoint}/historical-data/count",
                status_code=200,
                json={"count": 10},
                additional_matcher=get_match_request_auth_method(auth_settings),
            )
            count = api.count_predictions(activity_endpoint)
        assert count == 10


def test_atmospherex_get_predictions():
    for auth_settings in [None, AuthSettings("me", "me_subject", "secret")]:
        api = AtmospherexAPI(atmospherex_base_url, auth_settings)

        with requests_mock.Mocker(real_http=True) as mock_request:
            mock_prediction_requests(mock_request, auth_settings=auth_settings)
            predictions = list(api.get_predictions(activity_endpoint))
        assert len(predictions) == 150


def test_atmospherex_dump_predictions():
    for auth_settings in [None, AuthSettings("me", "me_subject", "secret")]:
        api = AtmospherexAPI(atmospherex_base_url, auth_settings)

        with requests_mock.Mocker(real_http=True) as mock_request:
            mock_prediction_requests(mock_request, auth_settings)
            api.dump_predictions(activity_endpoint, "test_dump_predictions.json")

        with open("test_dump_predictions.json", encoding=getdefaultencoding()) as fp:
            assert len(json.load(fp)["predictions"]) == 150

        os.remove("test_dump_predictions.json")
