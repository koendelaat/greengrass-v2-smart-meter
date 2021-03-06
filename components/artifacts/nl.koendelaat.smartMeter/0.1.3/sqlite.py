import datetime
import os.path
import sqlite3

import logging

logger = logging.getLogger(__name__)


def get_or_create_db(filename="consumption.db", create_script="createSQLiteDB.sql"):
    create_db = False
    filename = os.path.abspath(filename)
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        create_db = True
    logger.debug(f"Openening DB {filename}")
    con = sqlite3.connect(filename)

    if create_db:
        create_script = os.path.join(os.path.dirname(__file__), create_script)
        logger.info(f"Creating DB {filename} using {create_script}")
        cur = con.cursor()
        with open(create_script, 'rt') as f:
            script = f.read()
            cur.executescript(script)
        cur.close()

    return con


def add_consumption(con, dt, etotal):
    cur = con.cursor()
    cur.execute(f"INSERT INTO Consumption VALUES (?, ?)", (dt.timestamp(), int(etotal * 1000)))
    con.commit()
    cur.close()


def add_dummy_data(con):
    cur = con.cursor()
    for i in range(60):
        dt = datetime.datetime(2022, 3, 30, 21, i, 0)
        # 500W -> 0.5 kWh / 1h -> 1/120 kWh/1min
        power = 0.7  # kW
        etotal = 10000.0 + power*i/60

        cur.execute(f"INSERT INTO Consumption VALUES (?, ?)", (dt.timestamp(), int(etotal * 1000)))
    con.commit()
    cur.close()


def get_data(con, dt):
    cur = con.cursor()
    timestamp = dt.timestamp()
    max_timestamp = timestamp - (timestamp % 300)
    if timestamp % 300 < 150:
        max_timestamp -= 300
    for row in cur.execute(f"SELECT Nearest5min, CAST(strftime('%s', Nearest5min, 'UTC') AS datetime), PowerUsed FROM"
                           f" vwAvgConsumption WHERE CAST(strftime('%s', Nearest5min, 'UTC') AS datetime) > "
                           f"(SELECT LastUpdate FROM TempData) AND CAST(strftime('%s', Nearest5min, 'UTC')"
                           f" AS datetime) <= {max_timestamp}"):
        yield row
    cur.close()


def set_last_update(con, dt):
    cur = con.cursor()
    cur.execute(f"UPDATE TempData SET LastUpdate = {int(dt.timestamp())}")
    con.commit()
    cur.close()
