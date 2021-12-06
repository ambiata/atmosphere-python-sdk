from atmosphere.transformer.output_transformer import OutputTransformer
from atmosphere.transformer.pydantic_models import PredictionResponse


class TransformerForTest(OutputTransformer):
    def apply_transformation(self, msg) -> PredictionResponse:
        return PredictionResponse(action_name="test_action")


def test_transformer_tags_dict():
    """Make a sample transformer, see that tags is a dict"""
    test_transformer = TransformerForTest()
    assert isinstance(test_transformer.tags(), dict)


def test_empty_data():
    """Test sending in some empty data and check the output works"""

    test_transformer = TransformerForTest()
    result = test_transformer.transform_output_raw(
        {
            "data": {
                "names": ["a", "b"],
                "tensor": {"shape": [2, 2], "values": [0, 0, 1, 1]},
            }
        }
    )
    assert result["jsonData"] == {"action_name": "test_action", "logs": {}}
    # Metrics looks something like this:
    #     "meta": {
    #         "metrics": [
    #             {
    #                 "key": "transform_wall_time",
    #                 "type": "TIMER",
    #                 "value": 0.3581047058105469
    #             }
    #         ]
    #     }
    assert "metrics" in result["meta"]
    assert {"key", "type", "value"} == set(result["meta"]["metrics"][0])
    assert result["meta"]["metrics"][0]["key"] == "transform_wall_time"
    assert result["meta"]["metrics"][0]["type"] == "TIMER"
    assert result["meta"]["metrics"][0]["value"] > 0
