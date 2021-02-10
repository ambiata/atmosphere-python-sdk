from atmospherex_transformer_base.transformer import FeatureTransformer
from pydantic import BaseModel, Field, ValidationError
import numpy as np
import pytest

def test_transformer_tags_dict():
    """ Make a sample transformer, see that tags is a dict"""
    test_transformer = FeatureTransformer()
    assert isinstance(test_transformer.tags(), dict)

def test_empty_data():
    """ Test sending in some empty data and check the output works  """


    class TestTransformer(FeatureTransformer):

        def apply_transformation(self, msg):
            return np.array([], dtype=int)

    test_transformer = TestTransformer()
    result = test_transformer.transform_input_raw({
      "jsonData": {
        "context": {
        }
      }
    })
    assert result['data'] == {
        "names": [],
        "tensor": {
            "shape": (0, ),
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
