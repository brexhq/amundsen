# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

import logging

from http import HTTPStatus

from flask import Response, jsonify, make_response
from flask.blueprints import Blueprint

from amundsen_application.models.preview_data import (
    ColumnItem,
    PreviewData,
    PreviewDataSchema,
)

LOGGER = logging.getLogger(__name__)

freshness_blueprint = Blueprint('freshness', __name__, url_prefix='/api/freshness/v0')


@freshness_blueprint.route('/', methods=['POST'])
def get_table_freshness() -> Response:
    # fake data to test out functionality
    columns = [
        ColumnItem(column_name='latest updated_at', column_type=""),
        ColumnItem(column_name='latest inserted_at', column_type=""),
    ]
    rows_to_dicts = [
        {
            'latest updated_at': '2021-07-14 13:52:51.807 +0000',
            'latest inserted_at': '2021-07-13 10:01:03.302 +0000'
        }
    ]
    preview_data = PreviewData(columns, rows_to_dicts)

    data = PreviewDataSchema().dump(preview_data)
    payload = jsonify({'freshnessData': data, 'msg': 'Success'})
    import time
    time.sleep(5)
    return make_response(payload, HTTPStatus.OK)
