import logging

from starlette.status import HTTP_204_NO_CONTENT

from ..base_class import BaseActivityCustomCode
from ..pydantic_models import ComputeRewardResponse, Versions, PredictionResponsePayloadFormatListResponse, ExclusionRuleConditionListResponse, AppliedExclusionConditionsResponse
from ..version import get_base_version

logger = logging.getLogger(__name__)


class Endpoints:
    def __init__(self, router, module: BaseActivityCustomCode):
        self.router = router
        self.module = module
        # self.base_version = get_base_version()
        self.base_version = "3"
        self._init_routes()

    def get_versions(self) -> Versions:
        return Versions(
            base_version=self.base_version,
            module_version=self.module.get_module_version()
        )

    def _init_routes(self):
        self.router.add_api_route(
            "/validate-prediction-request",
            self.module.validate_prediction_request,
            methods=["POST"],
            status_code=HTTP_204_NO_CONTENT
        )
        self.router.add_api_route(
            "/validate-outcome-request",
            self.module.validate_outcome_request,
            methods=["POST"],
            status_code=HTTP_204_NO_CONTENT
        )
        self.router.add_api_route(
            "/compute-reward",
            self.module.compute_reward,
            methods=["POST"],
            response_model=ComputeRewardResponse
        )
        self.router.add_api_route(
            "/response-payload-formats",
            self.module.get_prediction_response_payload_formats,
            methods=["GET"],
            response_model=PredictionResponsePayloadFormatListResponse
        )
        self.router.add_api_route(
            "/format-prediction-payload-response",
            self.module.format_prediction_payload_response,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/versions",
            self.get_versions,
            methods=["GET"],
            response_model=Versions
        )
        self.router.add_api_route(
            "/exclusion-rule-conditions",
            self.module.get_exclusion_rule_conditions,
            methods=["GET"],
            response_model=ExclusionRuleConditionListResponse
        )
        self.router.add_api_route(
            "/applied-exclusion-conditions",
            self.module.get_applied_exclusion_conditions,
            methods=["POST"],
            response_model=AppliedExclusionConditionsResponse
        )