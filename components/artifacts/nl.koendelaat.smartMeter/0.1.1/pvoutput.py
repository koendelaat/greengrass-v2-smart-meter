from datetime import datetime

import requests


class PVOutput:
    def __init__(self, api_key, system_id):
        self.api_key = api_key
        self.system_id = system_id

        self.headers = {"x-pvoutput-apikey": str(self.api_key),
                        "x-pvoutput-systemid": str(self.system_id)}

    def add_consumption(self, dt: datetime, consumption_power, net=True):
        url = "https://pvoutput.org/service/r2/addstatus.jsp"

        request_url = f"{url}?d={dt.strftime('%Y%m%d')}&t={dt.strftime('%H:%M')}&n={int(net)}&v4={int(consumption_power)}"

        response = requests.get(request_url, headers=self.headers)

        return response
