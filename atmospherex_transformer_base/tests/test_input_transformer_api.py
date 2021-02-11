import json
from datetime import datetime

import numpy as np
from pydantic import BaseModel, Field

from atmospherex_transformer_base.input_transformer import InputTransformer
from atmospherex_transformer_base.pydantic_models import PredictionRequest
from .utils import get_test_app


def test_invalid_field():
    ''' Test invalid field, should get 422 error '''

    class TestModel(BaseModel):
        age: int = Field(..., ge=0, le=5, title='Age')

    class TestInputTransformer(InputTransformer):

        def apply_transformation(self, prediction_request: PredictionRequest):
            TestModel.parse_obj(prediction_request.source_request)
            return np.array([], dtype=int)

    app = get_test_app(TestInputTransformer())
    with app.test_client() as client:
        response = client.post('/transform-input', data=json.dumps({
            'jsonData': {
                'source_request': {
                    'age': 10
                },
                'prediction_timestamp': str(datetime.now())
            }
        }), content_type='application/json')
        assert response.status_code == 422
