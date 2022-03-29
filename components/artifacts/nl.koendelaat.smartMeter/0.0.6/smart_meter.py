import json

from dsmr_parser.clients import create_tcp_dsmr_reader
import logging

from dsmr_parser.objects import Telegram

logging.getLogger('dsmr_parser').setLevel(logging.INFO)


class DummyParser:
    def parse(self, telegram):
        return telegram


def create_connection(callback, loop):
    def telegram_callback(telegram):
        # telegram_dict = dict()
        # for obiref, obj in telegram.items():
        #     if obj:
        #         telegram_dict[obiref] = f"{obj.value} {obj.unit}"
        # callback(telegram_dict)

        callback(json.loads(Telegram(telegram, DummyParser(), None).to_json()))

    return create_tcp_dsmr_reader("alpha.home.local", 8000, '4', telegram_callback, loop)
