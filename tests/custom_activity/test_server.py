from copy import deepcopy

from fastapi.testclient import TestClient
from pytest import fixture

from atmosphere.custom_activity.server import server


@fixture(name="default_prediction")
def fixture_default_prediction():
    return {
        "atmosphere_call_uuid": "82fca11a-3c13-4e9f-93dc-8cbef03ab509",
        "info": {
            "activity": {
                "id": "c22d6e7a-fd33-4f60-8e5a-0a0ab9bb1da1",
                "name": "kana activity",
                "description": "Kana mock activity",
                "start_date": "2020-11-06T03:17:29.600944+00:00",
                "end_date": None,
                "status": "running",
                "current_category": "deployment",
                "endpoint": "my-awesome-activity",
            },
            "current_process": {
                "id": "5dd8356f-1b97-4fc2-9d4f-398bb4a7d239",
                "name": "kana",
                "description": "Kana mock",
                "category": "deployment",
                "start_date": "2020-11-06T03:17:29.600944+00:00",
                "end_date": None,
                "status": "running",
            },
            "method": {
                "id": "71fc02ec-6628-4712-ab3c-bd53cf1bb339",
                "name": "method_1",
                "method_type": "seldon",
                "config": {
                    "deployment_name": "neural-linear-inference-graph",
                    "namespace": "atmosphere",
                    "gateway_endpoint": "host.docker.internal:8000",
                    "gateway": "istio",
                },
            },
            "action": {
                "id": "21f73431-3c0e-4355-9dc8-773fa389169f",
                "name": "baseline",
                "payload": {"name": "baseline"},
            },
            "allocation": {"current_phase": None, "allocation_random_number": None},
        },
        "predictions": {"name": "baseline"},
        "logs": {
            "applied_traffic_exclusion_rules": [
                {
                    "id": "71fc02ec-6628-4712-ab3c-bd53cf1bb338",
                    "exclusion_rule_condition_id": "is-new-car",
                }
            ],
            "entity_applied_exclusion_conditions": [],
            "inference": {},
            "filtered_action_pool": {},
        },
    }


@fixture(name="test_client")
def fixture_test_client() -> TestClient:
    return TestClient(server)


def test_entrypoint_test(client: TestClient):
    resp = client.get("/versions")
    assert resp.status_code == 200
    assert len(resp.json()["base_version"]) > 0
    assert len(resp.json()["module_version"]) > 0


def test_get_prediction_response_payload_formats(test_client: TestClient):
    resp = test_client.get("/response-payload-formats")
    assert resp.status_code == 200
    assert resp.json() == {"prediction_response_payload_formats": []}


def test_format_prediction_payload_response(
    test_client: TestClient, default_prediction: dict
):
    resp = test_client.post(
        "/format-prediction-payload-response",
        params={"payload_format": "test"},
        json=default_prediction,
    )
    assert resp.status_code == 200
    assert resp.json() == default_prediction


def test_format_prediction_payload_response_empty_method(
    test_client: TestClient, default_prediction: dict
):
    prediction = deepcopy(default_prediction)
    prediction["info"]["method"] = None
    resp = test_client.post(
        "/format-prediction-payload-response",
        params={"payload_format": "test"},
        json=prediction,
    )
    assert resp.status_code == 200
    assert resp.json() == prediction


def test_exclusion_rule_condition(test_client: TestClient):
    resp = test_client.get(
        "/exclusion-rule-conditions",
    )
    assert resp.status_code == 200
    assert resp.json() == {"exclusion_rule_conditions": []}


def test_applied_exclusion_conditions(test_client: TestClient):
    resp = test_client.post(
        "/applied-exclusion-conditions", json={"context": "context"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"applied_exclusion_conditions": []}


def test_bias_attribute_configs(test_client: TestClient):
    resp = test_client.get("/bias-attribute-configs")
    resp.raise_for_status()
    assert resp.status_code == 200
    assert resp.json() == {"bias_attribute_configs": []}
