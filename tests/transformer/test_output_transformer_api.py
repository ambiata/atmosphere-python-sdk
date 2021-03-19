from atmosphere.transformer.output_transformer import OutputTransformer
from atmosphere.transformer.pydantic_models import PredictionResponse
from .utils import get_test_app


def test_valid_request():
    class TestOutputTransformer(OutputTransformer):

        def apply_transformation(self, msg) -> PredictionResponse:
            return PredictionResponse(
                action_name="test_action"
            )

    app = get_test_app(TestOutputTransformer())
    with app.test_client() as client:
        response = client.post('/transform-output', json={
            "data": {"names": ["a", "b"], "tensor": {"shape": [2, 2], "values": [0, 0, 1, 1]}}
        }, content_type='application/json')
        assert response.status_code == 200, response
        assert response.json['jsonData']['action_name'] == 'test_action', response.json
