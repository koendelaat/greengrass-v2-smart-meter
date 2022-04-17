# MIT No Attribution
#
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import asyncio
import datetime
import json
import logging
import os
import sys

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

from pvoutput import PVOutput
from smart_meter import create_connection
from sqlite import get_or_create_db, get_data, add_consumption, set_last_update

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class IoTHandler:
    def __init__(self):
        self.thing_name = os.getenv('AWS_IOT_THING_NAME', "UNKNOWN")
        self.ipc_client = awsiot.greengrasscoreipc.connect()
        self.api_key = self.get_secret('pvoutput_api_key').get('api_key')
        if self.api_key is None:
            raise RuntimeError("No API key found")

        system_settings = self.get_secret('pvoutput_systems').get(self.thing_name, {})
        self.system_id = system_settings.get('system_id')
        if self.system_id is None:
            raise RuntimeError(f"No system_id found for {self.thing_name}")

        self.dsmr_version = system_settings.get('dsmr', '5')

    def publish_data(self, payload):
        try:
            publish_operation = self.ipc_client.new_publish_to_iot_core()
            publish_operation.activate(
                request=model.PublishToIoTCoreRequest(topic_name=f'smartmeter/{self.thing_name}/consumption',
                                                      qos='0',
                                                      payload=json.dumps(payload).encode()))

        except Exception as e:
            logger.error("Failed to publish message: " + repr(e))

    def get_secret(self, secret_id):
        try:
            get_secret_operation = self.ipc_client.new_get_secret_value()
            get_secret_operation.activate(request=model.GetSecretValueRequest(secret_id=secret_id))
            secret_response = get_secret_operation.get_response().result()
            json_value = json.loads(secret_response.secret_value.secret_string)
            get_secret_operation.close()
            return json_value
        except Exception:
            return dict()


def get_callback(db, iot_handler, pvoutput):
    def callback(telegram):
        message_timestamp = telegram.P1_MESSAGE_TIMESTAMP.value
        if iot_handler.dsmr_version == '5':
            if message_timestamp.second != 0:
                return
        else:
            if message_timestamp.second >= 10:
                return
        edt1 = telegram.ELECTRICITY_DELIVERED_TARIFF_1.value
        edt2 = telegram.ELECTRICITY_DELIVERED_TARIFF_2.value
        eut1 = telegram.ELECTRICITY_USED_TARIFF_1.value
        eut2 = telegram.ELECTRICITY_USED_TARIFF_2.value
        e_total = eut1 + eut2 - edt1 - edt2
        add_consumption(db, message_timestamp, e_total)

        iot_fields = ["P1_MESSAGE_TIMESTAMP", "ELECTRICITY_USED_TARIFF_1", "ELECTRICITY_USED_TARIFF_2",
                      "ELECTRICITY_DELIVERED_TARIFF_1", "ELECTRICITY_DELIVERED_TARIFF_2", "HOURLY_GAS_METER_READING"]
        telegram_s = json.loads(telegram.to_json())
        telegram_s = {k: v for k, v in telegram_s.items() if k in iot_fields}
        iot_handler.publish_data(telegram_s)

        last_dt = None
        for row in get_data(db_conn, message_timestamp):
            dt = datetime.datetime.fromtimestamp(row[1])
            response = pvoutput.add_consumption(dt, row[2])
            if response.ok:
                last_dt = dt
            else:
                iot_handler.publish_data(dict(error=dict(response_status_code=response.status_code,
                                                         response_reason=response.reason,
                                                         response_text=response,
                                                         request_url=response.url)))
        if last_dt:
            set_last_update(db_conn, last_dt)

    return callback


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    handler = IoTHandler()

    handler.publish_data("Startup!")
    db_conn = get_or_create_db()

    pvoutput = PVOutput(handler.api_key, handler.system_id)

    telegram_callback = get_callback(db_conn, handler, pvoutput)

    try:
        # connect and keep connected until interrupted by ctrl-c
        while True:
            # create serial or tcp connection
            conn = create_connection(telegram_callback, handler.dsmr_version, loop)
            transport, protocol = loop.run_until_complete(conn)
            # wait until connection it closed
            loop.run_until_complete(protocol.wait_closed())
            # wait 5 seconds before attempting reconnect
            loop.run_until_complete(asyncio.sleep(5))
    except KeyboardInterrupt:
        # cleanup connection after user initiated shutdown
        transport.close()
        loop.run_until_complete(asyncio.sleep(0))
    finally:
        db_conn.close()
        loop.close()

