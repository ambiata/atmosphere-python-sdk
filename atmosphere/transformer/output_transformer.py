import json
import time
from abc import ABC, abstractmethod

from seldon_core.user_model import SeldonComponent
from seldon_core.utils import construct_response_json

from .base_transformer import BaseTransformer
from .pydantic_models import PredictionResponse


class OutputTransformer(ABC, BaseTransformer, SeldonComponent):
    @abstractmethod
    def apply_transformation(self, msg) -> PredictionResponse:
        """Method to be implemented that runs the unique transformation code
        Our implementation of transform_input_raw runs our boilerplate and calls
        .apply_transformation()"""

    def transform_output_raw(self, msg):
        """
        Use when Seldon PredictiveUnitType is OUTPUT_TRANSFORMER
        """
        start_time = time.time()
        prediction_response = self.apply_transformation(msg)
        wall_time = time.time() - start_time

        return construct_response_json(
            self,
            True,
            msg,
            json.loads(prediction_response.json()),
            custom_metrics=[
                {
                    "type": "TIMER",
                    "key": "transform_wall_time",
                    "value": wall_time * 1000,
                }
            ],
        )
