import datetime
import os

from data.config import NEXT_RUN_WAITING


TIMESTAMP_FILE = './data/last_run_UTC_timestamp.txt'


def save_timestamp() -> None:
    timestamp = datetime.datetime.now(datetime.UTC).timestamp()
    with open(TIMESTAMP_FILE, 'w') as f:
        f.write(str(timestamp))


def read_timestamp() -> float | None:
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, 'r') as f:
            timestamp = float(f.read().strip())
        return timestamp
    else:
        return None


def seconds_from_last_run() -> float:
    last_run = read_timestamp()
    return datetime.datetime.now(datetime.UTC).timestamp() - last_run