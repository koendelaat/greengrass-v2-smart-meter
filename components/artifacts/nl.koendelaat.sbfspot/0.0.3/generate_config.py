import json
import os
from string import Template

import awsiot
import awsiot.greengrasscoreipc.model as model


class PVOutputConfig:
    def __init__(self, ipc_client, template_file, config_file):
        self.thing_name = os.getenv('AWS_IOT_THING_NAME', "UNKNOWN")
        self.ipc_client = ipc_client
        self.api_key = self.get_secret('pvoutput_api_key').get('api_key')
        self.system_config = self.get_secret('pvoutput_systems').get(self.thing_name, {})
        if self.api_key is None:
            raise RuntimeError("No API key found")
        if self.system_config is None:
            raise RuntimeError(f"No system config found for {self.thing_name}")

        self.template_file = os.path.join(os.path.dirname(__file__), template_file)
        self.config_file = os.path.abspath(config_file)

        with open(self.template_file, 'rt') as f:
            self.template = Template(f.read())

        # result = self.template.substitute(d)
        # print(result)

    def write(self):
        values = dict(thing_name=self.thing_name, ip_address=self.system_config.get("ip_address"),
                      password=self.system_config.get('password'), api_key=self.api_key,
                      sid=f"{self.system_config.get('serial')}:{self.system_config.get('system_id')}")
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'wt') as f:
            f.write(self.template.substitute(values))

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


class PVOutputConfigDummy(PVOutputConfig):
    def get_secret(self, secret_id):
        secrets = {
            "pvoutput_systems": {
                "MyThing": {
                    "system_id": 12345,
                    "password": "***REMOVED***",
                    "ip_address": "192.168.178.165",
                    "serial": 1234567890
                }
            },
            "pvoutput_api_key": {
                    "api_key": "***REMOVED***"
            }
        }
        return secrets.get(secret_id, {})


if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()
    PVOutputConfigDummy(ipc_client, template_file='SBFspot.tpl', config_file='config/SBFspot.cfg').write()
    PVOutputConfigDummy(ipc_client, template_file='SBFspotUpload.tpl', config_file='config/SBFspotUpload.cfg').write()
