from dataclasses import dataclass

from fastapi.testclient import TestClient

from atmosphere.custom_activity.pydantic_models import ComputeRewardResponse, Versions

from ..activity_for_tests import ActivityCustomCodeForTest, ExpectedModel


@dataclass(frozen=True)
class Example:
    a: str = "abc"
    b: int = 3
    good_prediction: ExpectedModel = ExpectedModel(a=a, b=b)


def test_validate_prediction(client: TestClient) -> None:
    response = client.post(
        "/validate-prediction-request", json=Example.good_prediction.dict()
    )
    assert response.status_code == 204


def test_validate_prediction_not_valid(client: TestClient) -> None:
    _failed_validation(client, "/validate-prediction-request")


def test_validate_outcome(client: TestClient) -> None:
    response = client.post(
        "/validate-outcome-request", json=Example.good_prediction.dict()
    )
    assert response.status_code == 204


def test_validate_outcome_not_valid(client: TestClient) -> None:
    _failed_validation(client, "/validate-outcome-request")


def test_compute_rewards(client: TestClient) -> None:
    response = client.post("/compute-reward", json=Example.good_prediction.dict())
    assert response.status_code == 200
    # Raise an exception if not if the model does not validate the payload
    compute_reward_response = ComputeRewardResponse.parse_obj(response.json())
    assert compute_reward_response.reward == Example.b


def test_versions(client: TestClient) -> None:
    response = client.get("/versions")
    assert response.status_code == 200
    # Raise an exception if not if the model does not validate the payload
    compute_reward_response = Versions.parse_obj(response.json())
    assert len(compute_reward_response.base_version) > 0
    assert (
        compute_reward_response.module_version
        == ActivityCustomCodeForTest.expected_module_version
    )


def _failed_validation(client, path):
    # Missing a field
    data = {"a": "abc"}
    response = client.post(path, json=data)
    assert response.status_code == 422

    # Extra field
    data = Example.good_prediction.dict()
    data["c"] = 2
    response = client.post(path, json=data)
    assert response.status_code == 422

    # Wrong type
    data = Example.good_prediction.dict()
    data["b"] = "def"
    response = client.post(path, json=data)
    assert response.status_code == 422
