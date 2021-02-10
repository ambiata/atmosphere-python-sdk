from atmospherex_transformer_base.transformer import FeatureTransformer
from pydantic import BaseModel, Field
import numpy as np
import json
import pytest
from .utils import get_test_app

def client():
    seldon_metrics = SeldonMetrics(worker_id_func=os.getpid)

    pass

def test_invalid_field():
    ''' Test invalid field, should get 422 error '''

    class TestModel(BaseModel):
        age: int = Field(..., ge=0, le=5, title='Age')


    class TestTransformer(FeatureTransformer):

        def apply_transformation(self, msg):
            TestModel.parse_obj(msg["jsonData"]["context"])
            return np.array([], dtype=int)

    app = get_test_app(TestTransformer())
    with app.test_client() as client:
        response = client.post('/transform-input', data=json.dumps({
            'jsonData': {
                'context': {
                    'age': 10
                }
            }
        }), content_type='application/json')
        assert response.status_code == 422
