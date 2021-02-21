from fastapi.testclient import TestClient

from atmosphere.activity.server import server

default_prediction_example = {
    'atmosphere_call_uuid': '82fca11a-3c13-4e9f-93dc-8cbef03ab509',
    'info': {
        'activity': {
            'id': 'c22d6e7a-fd33-4f60-8e5a-0a0ab9bb1da1',
            'name': 'kana activity',
            'description': 'Kana mock activity',
            'start_date': '2020-11-06T03:17:29.600944+00:00',
            'end_date': None,
            'status': 'running',
            'current_category': 'deployment',
            'endpoint': 'my-awesome-activity'
        },
        'current_process': {
            'id': '5dd8356f-1b97-4fc2-9d4f-398bb4a7d239',
            'name': 'kana',
            'description': 'Kana mock',
            'category': 'deployment',
            'start_date': '2020-11-06T03:17:29.600944+00:00',
            'end_date': None,
            'status': 'running'
        },
        'method': {
            'id': '71fc02ec-6628-4712-ab3c-bd53cf1bb339',
            'name': 'method_1',
            'method_type': 'seldon',
            'config': {
                'deployment_name': 'neural-linear-inference-graph',
                'namespace': 'atmosphere',
                'gateway_endpoint': 'host.docker.internal:8000',
                'gateway': 'istio'
            }
        },
        'action': {
            'id': '21f73431-3c0e-4355-9dc8-773fa389169f',
            'name': 'baseline',
            'payload': {
                'name': 'baseline'
            }
        },
        'allocation': {
            'current_phase': None,
            'allocation_random_number': None
        }
    },
    'predictions': {
        'name': 'baseline'
    },
    'logs': {}
}


def test_entrypoint_test():
    test_client = TestClient(server)
    resp = test_client.get('/versions')
    assert resp.status_code == 200


def test_get_prediction_response_payload_formats():
    test_client = TestClient(server)
    resp = test_client.get('/response-payload-formats')
    assert resp.status_code == 200
    assert resp.json() == {"prediction_response_payload_formats": []}


def test_format_prediction_payload_response():
    test_client = TestClient(server)
    resp = test_client.post(
        '/format-prediction-payload-response',
        params={"payload_format": "test"},
        json=default_prediction_example
    )
    assert resp.status_code == 200
    assert resp.json() == default_prediction_example


def test_exclusion_rule_condition():
    test_client = TestClient(server)
    resp = test_client.get(
        '/exclusion-rule-conditions',
    )
    assert resp.status_code == 200
    assert resp.json() == {'exclusion_rule_conditions': []}


def test_applied_exclusion_conditions():
    test_client = TestClient(server)
    resp = test_client.post(
        '/applied-exclusion-conditions',
        json={"context": "context"}
    )
    assert resp.status_code == 200
    assert resp.json() == {'applied_exclusion_conditions': []}
