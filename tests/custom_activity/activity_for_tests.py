from typing import Tuple

import requests
from pydantic import BaseModel
from requests.models import Response

from atmosphere.custom_activity import BaseActivityCustomCode
from atmosphere.custom_activity.pydantic_models import ComputeRewardResponse

prediction_extra_info = {"extra": "inf", "awesome_value": 42}


class ExpectedModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    a: str
    b: int


class ActivityCustomCodeForTest(BaseActivityCustomCode):
    base_version = "base_version_xyz"
    expected_module_version = "0.4.2"

    def validate_prediction_request(self, prediction_request: dict) -> None:
        ExpectedModel.model_validate(prediction_request)

    def validate_outcome_request(self, outcome_request: dict) -> None:
        ExpectedModel.model_validate(outcome_request)

    def compute_reward(self, outcome_request: dict) -> ComputeRewardResponse:
        outcome = ExpectedModel.model_validate(outcome_request)
        return ComputeRewardResponse(reward=outcome.b)

    def get_module_version(self) -> str:
        return self.expected_module_version

    def send_mock_prediction_request(
        self, url_prediction_endpoint: str
    ) -> Tuple[Response, dict]:
        return (
            requests.post(
                url_prediction_endpoint,
                json=ExpectedModel(a="a", b=3).model_dump(),
                timeout=5,
            ),
            prediction_extra_info,
        )

    def send_mock_outcome_request(
        self,
        url_outcome_endpoint: str,
        prediction_response: Response,
        info_from_prediction: dict,
    ) -> Response:
        assert info_from_prediction == prediction_extra_info
        return requests.post(
            url_outcome_endpoint, json=ExpectedModel(a="b", b=2).model_dump(), timeout=5
        )
