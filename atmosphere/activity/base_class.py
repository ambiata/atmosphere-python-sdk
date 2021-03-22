from abc import ABC, abstractmethod
from typing import Tuple

from requests import Response

from .pydantic_models import (AppliedExclusionConditionsResponse,
                              ComputeRewardResponse, DefaultPredictionResponse,
                              ExclusionRuleConditionListResponse,
                              PredictionResponsePayloadFormatListResponse)


class BaseActivityCustomCode(ABC):
    """
    The main class of this repository: the one to be implemented
    """

    is_for_mocker: bool

    def __init__(self, is_for_mocker: bool = False):
        self.is_for_mocker = is_for_mocker

    @abstractmethod
    def validate_prediction_request(self, prediction_request: dict) -> None:
        """Raise a ValidationError if the received prediction request is not valid"""

    @abstractmethod
    def validate_outcome_request(self, outcome_request: dict) -> None:
        """Raise a ValidationError if the received outcome request is not valid"""

    @abstractmethod
    def compute_reward(self, outcome_request: dict) -> ComputeRewardResponse:
        """From an outcome, compute the reward"""

    @abstractmethod
    def get_module_version(self) -> str:
        """Return the version of the module."""

    @abstractmethod
    def send_mock_prediction_request(
        self, url_prediction_endpoint: str
    ) -> Tuple[Response, dict]:
        """
        Send a mock request to the provided url and returns the corresponding response
        with extra information if required for computing the prediction.
        The response and dictionary will be provided to
        the `send_mock_outcome_request`.
        """

    @abstractmethod
    def send_mock_outcome_request(
        self,
        url_outcome_endpoint: str,
        prediction_response: Response,
        info_from_prediction: dict,
    ) -> Response:
        """
        Send a mock request to the provided url and returns the corresponding response.
        Provide the prediction response and extra information created while
        creating the prediction request from `send_mock_prediction_request`.
        """

    def get_prediction_response_payload_formats(
        self,
    ) -> PredictionResponsePayloadFormatListResponse:
        """
        Return the list of available format of the prediction payload.
        Every format should have a name and a description
        The name of the format should be unique.
        """
        return {"prediction_response_payload_formats": []}

    def format_prediction_payload_response(
        self,
        default_prediction_response: DefaultPredictionResponse,
        payload_format: str,  # noqa pylint: disable=unused-argument
    ) -> dict:
        """
        You can format the prediction the way you want based
        on the information returned by default
        """
        return default_prediction_response

    def get_exclusion_rule_conditions(self) -> ExclusionRuleConditionListResponse:
        """
        Define the exclusion rules for the activity
        """
        return ExclusionRuleConditionListResponse(exclusion_rule_conditions=[])

    def get_applied_exclusion_conditions(
        self, prediction_request: dict  # noqa pylint: disable=unused-argument
    ) -> AppliedExclusionConditionsResponse:
        """
        Define the exclusion rules for the activity
        """
        return AppliedExclusionConditionsResponse(applied_exclusion_conditions=[])
