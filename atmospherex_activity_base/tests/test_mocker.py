import datetime
import json
import unittest
from unittest.mock import Mock, patch

import httpretty

from atmospherex_activity_base.mocker import main_mocker
from atmospherex_activity_base.mocker.mocker import Mocker
from atmospherex_activity_base.mocker.mocker_config import MockerConfig


class TestMocker(unittest.TestCase):
    mocker_config = MockerConfig()
    mocker = Mocker(mocker_config)

    @httpretty.activate
    def test_sending_prediction_and_outcome(self):
        expected_prediction = {"atmosphere_call_uuid": "abc-123"}
        httpretty.register_uri(
            httpretty.POST,
            "http://mocker-test-url.atmospherex/predictions",
            body=json.dumps(expected_prediction)
        )
        httpretty.register_uri(
            httpretty.POST,
            "http://mocker-test-url.atmospherex/outcomes",
            status=204
        )

        prediction_response, extra_info = self.mocker.send_prediction()
        self.assertEqual(prediction_response.status_code, 200)
        self.assertEqual(prediction_response.json(), expected_prediction)

        outcome_response = self.mocker.send_outcome(prediction_response, extra_info)
        self.assertEqual(outcome_response.status_code, 204)

    @patch('random.uniform', lambda min, max: 1)
    @patch('atmospherex_activity_base.mocker.mocker.datetime')
    def test_outcome_time_some(self, mock_datetime):
        mock_datetime.now = Mock(return_value=datetime.datetime(2019, 1, 1, 0, 0, 0))
        self.assertEqual(datetime.datetime(2019, 1, 1, 0, 0, 1), self.mocker.get_outcome_time())

    @patch('random.uniform', lambda min, max: 90)
    def test_outcome_time_none_if_random_exceeds_timeout(self):
        self.assertEqual(self.mocker.get_outcome_time(), None)

    def test_entrypoint_tester(self):
        main_mocker.main(True)
