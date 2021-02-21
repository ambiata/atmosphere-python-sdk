import os
from typing import Optional

from ..base_config import Config


class MockerConfig(Config):
    activity_inference_base_url: str
    outcomes_rate: float
    outcomes_timeout_seconds: int
    requests_per_second: float
    max_predictions: Optional[int]

    def __init__(self):
        super(MockerConfig, self).__init__()
        self.activity_inference_base_url = os.environ["ACTIVITY_INFERENCE_BASE_URL"]
        self.outcomes_rate = float(os.environ["OUTCOMES_RATE"])
        self.outcomes_timeout_seconds = int(os.environ["OUTCOMES_TIMEOUT_SECONDS"])
        self.requests_per_second = float(os.environ["REQUESTS_PER_SECOND"])
        self.max_predictions = int(os.environ["MAX_PREDICTIONS"]) if "MAX_PREDICTIONS" in os.environ else None
