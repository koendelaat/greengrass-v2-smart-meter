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
import json
import logging
import os
import sys

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

from smart_meter import create_connection

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class IoTHandler:
    def __init__(self):
        self.thing_name = os.getenv('AWS_IOT_THING_NAME')
        self.ipc_client = awsiot.greengrasscoreipc.connect()
        self.api_key = self.get_secret('pvoutput_api_key').get('api_key')
        if self.api_key is None:
            raise RuntimeError("No API key found")

        self.system_id = self.get_secret('pvoutput_systems').get(self.thing_name, {}).get('system_id')
        if self.system_id is None:
            raise RuntimeError(f"No system_id found for {self.thing_name}")

    def publish_data(self, data=None):
        try:
            if data is None:
                payload = {
                    'api_key': self.api_key,
                    'system_id': self.system_id
                }
                payload.update(os.environ)
            else:
                payload = data

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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    handler = IoTHandler()
    handler.publish_data("Startup!")
    callback = handler.publish_data

    try:
        # connect and keep connected until interrupted by ctrl-c
        while True:
            # create serial or tcp connection
            conn = create_connection(callback, loop)
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
        loop.close()

