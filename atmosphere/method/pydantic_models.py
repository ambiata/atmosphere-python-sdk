from datetime import datetime
from typing import Dict, Optional, Set

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    source_request: Dict = Field(
        ...,
        title="Source request",
        description="Source request received by AtmosphereX from external system.",
    )
    prediction_timestamp: datetime = Field(
        ...,
        title="Prediction time",
        description="Time when the prediction was requested.",
    )
    allowed_action_names: Optional[Set[str]] = Field(
        None,
        title="Set of allowed actions",
        description="Set of actions that the inference pipeline can return."
        "If the list is empty or absent, any actions can be returned,"
        "otherwise any actions not in this list will be discarded by AtmosphereX"
        "which will return a default value. The set contains the action names only.",
    )


class PredictionResponse(BaseModel):
    class Config:
        ignore_extra = False

    action_name: str = Field(
        ..., title="Action name", description="Prediction action name"
    )
    logs: Dict = Field(
        {},
        title="Prediction logs",
        description="Logs created by the inference endpoints which will be stored "
        "in the database with the corresponding prediction.",
    )
