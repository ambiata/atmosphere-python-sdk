import json
import os

import requests_mock

from atmosphere.atmospherex import AtmospherexAPI

atmospherex_base_url = "http://atmospherex.base-url.com"
activity_endpoint = "conversation-rate-optimisation"


def mock_prediction_requests(mock_request):
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data/count",
        status_code=200,
        json={"count": 150},
    )
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data",
        status_code=200,
        json={
            "predictions": [{"user": "James", "order": "spicy meatball sandwich"}] * 100
        },
    )
    mock_request.register_uri(
        "GET",
        f"{atmospherex_base_url}/api"
        f"/inferences/{activity_endpoint}/historical-data?skip=100",
        status_code=200,
        json={
            "predictions": [{"user": "Jim", "order": "spicy meatball sandwich"}] * 50
        },
    )


def test_atmospherex_count():
    api = AtmospherexAPI(atmospherex_base_url)
    with requests_mock.Mocker(real_http=True) as mock_request:
        mock_request.register_uri(
            "GET",
            f"{atmospherex_base_url}/api"
            f"/inferences/{activity_endpoint}/historical-data/count",
            status_code=200,
            json={"count": 10},
        )
        count = api.count_predictions(activity_endpoint)
    assert count == 10


def test_atmospherex_get_predictions():
    api = AtmospherexAPI(atmospherex_base_url)
    with requests_mock.Mocker(real_http=True) as mock_request:
        mock_prediction_requests(mock_request)
        predictions = list(api.get_predictions(activity_endpoint))
    assert len(predictions) == 150


def test_atmospherex_dump_predictions():
    api = AtmospherexAPI(atmospherex_base_url)

    with requests_mock.Mocker(real_http=True) as mock_request:
        mock_prediction_requests(mock_request)
        api.dump_predictions(activity_endpoint, "test_dump_predictions.json")

    with open("test_dump_predictions.json") as fp:
        assert len(json.load(fp)["predictions"]) == 150

    os.remove("test_dump_predictions.json")
