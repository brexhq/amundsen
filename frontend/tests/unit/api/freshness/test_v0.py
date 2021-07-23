# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

import unittest
import json
from http import HTTPStatus
from typing import Dict

from flask import Response

from amundsen_application import create_app
from amundsen_application.api.freshness import v0
from amundsen_application.base.base_data_freshness_client import BaseDataFreshnessClient

local_app = create_app('amundsen_application.config.TestConfig', 'tests/templates')
DATA_FRESHNESS_CLIENT_CLASS = 'tests.unit.api.freshness.test_v0.DataFreshnessClient'


class DataFreshnessClient(BaseDataFreshnessClient):
    def __init__(self) -> None:
        pass

    def get_freshness_data(self, params: Dict, optionalHeaders: Dict = None) -> Response:
        pass


class DataFreshnessTest(unittest.TestCase):

    def setUp(self) -> None:
        local_app.config['PREVIEW_CLIENT_ENABLED'] = True

    def test_no_client_class(self) -> None:
        """
        Test that Not Implemented error is raised when FRESHNESS_CLIENT is None
        :return:
        """
        # Reset side effects of other tests to ensure that the results are the
        # same regardless of execution order
        v0.DATA_FRESHNESS_CLIENT_CLASS = None
        v0.DATA_FRESHNESS_CLIENT_INSTANCE = None

        local_app.config['DATA_FRESHNESS_CLIENT'] = None
        with local_app.test_client() as test:
            response = test.post('/api/freshness/v0/')
            self.assertEqual(response.status_code, HTTPStatus.NOT_IMPLEMENTED)

    @unittest.mock.patch(DATA_FRESHNESS_CLIENT_CLASS + '.get_freshness_data')
    def test_good_client_response(self, mock_get_freshness_data: unittest.mock.Mock) -> None:
        """
        Test response
        """
        expected_response_json = {
            'msg': 'Success',
            'freshnessData': {
                'columns': [{}, {}],
                'data': [{'latest updated_at': '2021-07-14 13:52:51.807 +0000'}]}
        }

        local_app.config['DATA_FRESHNESS_CLIENT'] = DATA_FRESHNESS_CLIENT_CLASS
        response = json.dumps({'freshness_data': {
            'columns': [{}, {}],
            'data': [{'latest updated_at': '2021-07-14 13:52:51.807 +0000'}]
        }})
        mock_get_freshness_data.return_value = Response(response=response,
                                                        status=HTTPStatus.OK)
        with local_app.test_client() as test:
            post_response = test.post('/api/freshness/v0/')
            self.assertEqual(post_response.status_code, HTTPStatus.OK)
            self.assertEqual(post_response.json, expected_response_json)
