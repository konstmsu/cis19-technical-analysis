from contextlib import contextmanager
import os
from datetime import timedelta, datetime


def _set_timestamp(test_name, moment: datetime):
    file_name = _get_filename(test_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w+") as file:
        file.write(moment.isoformat())


def _get_timestamp(test_name):
    file_name = _get_filename(test_name)
    if not os.path.isfile(file_name):
        return datetime.min

    with open(file_name, "r") as file:
        return datetime.fromisoformat(file.readline())


def _get_filename(test_name):
    return os.path.join("_test_timestamps", test_name)


def _now():
    return datetime.utcnow()


def _skip_test(test_name, max_age):
    return _get_timestamp(test_name) + max_age >= _now()


@contextmanager
def skip_slow_test(test_name, max_age: timedelta):
    yield _skip_test(test_name, max_age)
    _set_timestamp(test_name, _now())
