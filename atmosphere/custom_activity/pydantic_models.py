from datetime import datetime
from typing import List, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel


class BaseModelForbiddingExtraFields(BaseModel):
    class Config:
        extra = "forbid"


class ComputeRewardResponse(BaseModelForbiddingExtraFields):
    reward: float


class Versions(BaseModelForbiddingExtraFields):
    base_version: str
    module_version: str


class PredictionResponsePayloadFormat(BaseModel):
    name: str
    description: Optional[str]


class PredictionResponsePayloadFormatListResponse(BaseModel):
    prediction_response_payload_formats: List[PredictionResponsePayloadFormat]


class Phase(BaseModel):
    id: UUID
    name: str
    description: str
    status: str
    start_date: datetime
    end_date: Optional[datetime]


class Activity(BaseModel):
    id: UUID
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime]
    status: str
    current_category: str
    endpoint: str


class Process(BaseModel):
    id: UUID
    name: str
    description: str
    category: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str


class Method(BaseModel):
    id: UUID
    name: str
    method_type: str
    config: Optional[dict]


class Action(BaseModel):
    id: UUID
    name: str
    payload: dict


class AllocationLog(BaseModel):
    current_phase: Optional[Phase] = None
    allocation_random_number: Optional[float] = None


class InferenceInfo(BaseModel):
    activity: Activity
    current_process: Process
    method: Method
    action: Action
    allocation: AllocationLog


class DefaultPredictionResponse(BaseModel):
    atmosphere_call_uuid: UUID
    info: InferenceInfo
    predictions: dict
    logs: dict


class ExclusionRuleCondition(BaseModel):
    id: str
    name: str
    description: str


class ExclusionRuleConditionResponse(BaseModel):
    exclusion_rule_condition: ExclusionRuleCondition


class ExclusionRuleConditionListResponse(BaseModel):
    exclusion_rule_conditions: List[ExclusionRuleCondition]


class AppliedExclusionConditionsResponse(BaseModel):
    applied_exclusion_conditions: List[ExclusionRuleCondition]


class BiasAttributeType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"


class BiasAttributeConfig(BaseModel):
    name: str
    path: str # The path is a json path, eg. "context.age"
    attribute_type: BiasAttributeType


class BiasAttributeConfigListResponse(BaseModel):
    ''' The custom activity returns the bias attribute configs
    that atmospherex uses to decide which fields may be used
    for bias attributes '''
    bias_attribute_configs: List[BiasAttributeConfig]
