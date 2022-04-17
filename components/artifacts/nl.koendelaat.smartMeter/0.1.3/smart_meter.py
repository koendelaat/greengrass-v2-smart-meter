import json

from dsmr_parser.clients import create_tcp_dsmr_reader, create_dsmr_reader
import logging

from dsmr_parser.objects import Telegram

logging.getLogger('dsmr_parser').setLevel(logging.INFO)


class DummyParser:
    def parse(self, telegram):
        return telegram


def create_connection(callback, dsmr_version, loop):
    def telegram_callback(telegram):
        callback(Telegram(telegram, DummyParser(), None))

    # return create_tcp_dsmr_reader("alpha.home.local", 8000, '4', telegram_callback, loop)
    return create_dsmr_reader("/dev/ttyUSB0", dsmr_version, telegram_callback, loop)
