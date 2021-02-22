from datetime import datetime

import numpy as np

from atmosphere.transformer.input_transformer import InputTransformer
from atmosphere.transformer.pydantic_models import PredictionRequest


class TransformerForTest(InputTransformer):

    def apply_transformation(self, prediction_request: PredictionRequest):
        return np.array([], dtype=int)


def test_transformer_tags_dict():
    """ Make a sample transformer, see that tags is a dict"""
    test_transformer = TransformerForTest()
    assert isinstance(test_transformer.tags(), dict)


def test_empty_data():
    """ Test sending in some empty data and check the output works  """

    test_transformer = TransformerForTest()
    result = test_transformer.transform_input_raw({
        "jsonData": {
            "source_request": {
            },
            'prediction_timestamp': datetime.now()
        }
    })
    assert result['data'] == {
        "names": [],
        "tensor": {
            "shape": (0,),
            "values": []
        }
    }
    '''
    Metrics looks something like this:
        "meta": {
            "metrics": [
                {
                    "key": "transform_wall_time",
                    "type": "TIMER",
                    "value": 0.3581047058105469
                }
            ]
        }
    '''
    assert 'metrics' in result['meta']
    assert {'key', 'type', 'value'} == set(result['meta']['metrics'][0])
    assert result['meta']['metrics'][0]['key'] == 'transform_wall_time'
    assert result['meta']['metrics'][0]['type'] == 'TIMER'
    assert result['meta']['metrics'][0]['value'] > 0
