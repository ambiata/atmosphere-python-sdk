import time
from abc import ABC, abstractmethod
from typing import Any, Dict

import numpy as np
from seldon_core.user_model import SeldonComponent
from seldon_core.utils import construct_response_json

from .base_transformer import BaseTransformer
from .pydantic_models import PredictionRequest


class InputTransformer(ABC, BaseTransformer, SeldonComponent):
    @abstractmethod
    def apply_transformation(self, prediction_request: PredictionRequest) -> np.ndarray:
        """Method to be implemented that runs the unique transformation code
        Our implementation of transform_input_raw runs our boilerplate and calls
        .apply_transformation()"""

    def transform_input_raw(self, msg: Dict[str, Any]):
        """
        Use when Seldon PredictiveUnitType is TRANSFORMER
        """
        start_time = time.time()
        prediction_request = PredictionRequest.parse_obj(msg["jsonData"])
        result_np_array = self.apply_transformation(prediction_request)
        wall_time = time.time() - start_time

        return construct_response_json(
            self,
            True,
            msg,
            result_np_array,
            custom_metrics=[
                {
                    "type": "TIMER",
                    "key": "transform_wall_time",
                    "value": wall_time * 1000,
                }
            ],
        )
