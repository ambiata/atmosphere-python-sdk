import logging
import random
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from requests import Response

from ..module_importer import get_module_constructor
from .mocker_config import MockerConfig


def status_ok(response: Response):
    return 200 <= response.status_code < 300


class Mocker:
    logger = logging.getLogger(__name__)

    def __init__(self, mocker_config: MockerConfig):
        self.mocker_config = mocker_config
        module_constructor = get_module_constructor(mocker_config)
        self.module = module_constructor(is_for_mocker=True)
        self.scheduler = BackgroundScheduler()
        self.finished = False
        self.report_printed = False
        self.predictions_accepted = 0
        self.predictions_rejected = 0
        self.outcomes_accepted = 0
        self.outcomes_rejected = 0

    def start(self):
        self.scheduler.start()
        try:
            while True:
                time.sleep(1 / self.mocker_config.requests_per_second)
                self.single_task()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def single_task(self):
        if self.is_finished():
            self.print_report_when_done()
            return

        self.scheduler.add_job(self.send_prediction)

    def send_outcome(self, prediction_response: Response, prediction_information: dict):
        response = self.module.send_mock_outcome_request(
            f"{self.mocker_config.activity_inference_base_url}/outcomes",
            prediction_response,
            prediction_information,
        )
        self.logger.info("Outcome posted: %s", response.status_code)
        if status_ok(response):
            self.outcomes_accepted += 1
        else:
            self.outcomes_rejected += 1
        return response

    def send_prediction(self):
        response, prediction_info = self.module.send_mock_prediction_request(
            f"{self.mocker_config.activity_inference_base_url}/predictions"
        )
        if status_ok(response):
            self._successful_prediction(response, prediction_info)
        else:
            self._failed_prediction(response)
        return response, prediction_info

    def _successful_prediction(self, prediction, prediction_info) -> None:
        self.predictions_accepted += 1
        outcome_time = self.get_outcome_time()
        if outcome_time is not None:
            self.scheduler.add_job(
                self.send_outcome,
                "date",
                run_date=outcome_time,
                args=[prediction, prediction_info],
            )
            self.logger.info(
                "Prediction received, will send outcome at %s", outcome_time
            )
        else:
            self.logger.info("Prediction received, no outcome")

    def _failed_prediction(self, prediction) -> None:
        self.predictions_rejected += 1
        self.logger.error(
            "Error requesting prediction. Status=%s Message=%s",
            prediction.status_code,
            prediction.text,
        )

    def is_finished(self) -> bool:
        return self.mocker_config.max_predictions and (
            0
            < self.mocker_config.max_predictions
            <= self.predictions_accepted + self.predictions_rejected
        )

    def get_outcome_time(self):
        if self.mocker_config.outcomes_rate == 0:
            return None

        delay_outcome_seconds = random.uniform(
            0,
            self.mocker_config.outcomes_timeout_seconds
            / self.mocker_config.outcomes_rate,
        )

        if self.mocker_config.outcomes_timeout_seconds < delay_outcome_seconds:
            return None

        return datetime.now() + timedelta(seconds=delay_outcome_seconds)

    def print_report_when_done(self) -> None:
        if self.report_printed:
            return
        # if there are still some jobs in the queue, we will wait for them
        # to finish before printing the reports as we
        # still have some requests to send.
        while self._has_jobs_left_in_queue():
            time.sleep(0.1)
        self.logger.info("%s mock complete", type(self.module).__name__)
        self.logger.info("Predictions accepted: %s", self.predictions_accepted)
        self.logger.info("Predictions rejected: %s", self.predictions_rejected)
        self.logger.info("Outcomes accepted: %s", self.outcomes_accepted)
        self.logger.info("Outcomes rejected: %s", self.outcomes_rejected)
        self.report_printed = True

    def _has_jobs_left_in_queue(self) -> bool:
        return len(self.scheduler.get_jobs()) != 0
