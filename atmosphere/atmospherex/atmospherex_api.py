import math
from datetime import datetime
from typing import Generator

import requests

BATCH_LIMIT = 100


class AtmospherexAPI:
    """
    This is the main class you instantiate to access the AtmosphereX API
    """

    def __init__(self, atmospherex_base_url: str):
        """
        :param api_base_url: The base url of the atmospherex API
        """
        self.atmospherex_base_url = atmospherex_base_url

    def count_predictions(
        self,
        activity_endpoint: str,
        from_datetime: datetime = None,
        to_datetime: datetime = None,
    ) -> int:
        """
        Return the count of the predictions of the activity
        between from_datetime and to_datetime if provided

        :param activity_endpoint: the activity uniq endpoint
        :param from_datetime: consider predictions from this datetime
        :param to_datetime: consider predictions to this datetime
        """
        payload = {
            "start_prediction_date": from_datetime,
            "end_prediction_date": to_datetime,
        }
        url = (
            f"{self.atmospherex_base_url}/api"
            f"/inferences/{activity_endpoint}/historical-data/count"
        )
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response.json()["count"]

    def get_predictions(
        self,
        activity_endpoint: str,
        from_datetime: datetime = None,
        to_datetime: datetime = None,
    ) -> Generator:
        """
        Return a generator of predictions of the activity between
        from_datetime and to_datetime if provided

        :param activity_endpoint: the activity unique endpoint
        :param from_datetime: consider predictions from this datetime
        :param to_datetime: consider predictions to this datetime
        """
        count = self.count_predictions(activity_endpoint, from_datetime, to_datetime)
        url = (
            f"{self.atmospherex_base_url}/api"
            f"/inferences/{activity_endpoint}/historical-data"
        )
        for iteration in range(math.ceil(count / BATCH_LIMIT)):
            payload = {
                "start_prediction_date": from_datetime,
                "end_prediction_date": to_datetime,
                "skip": BATCH_LIMIT * iteration,
            }

            response = requests.get(url, params=payload)
            response.raise_for_status()
            yield from response.json()["predictions"]
