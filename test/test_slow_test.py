# pylint: disable=protected-access
from datetime import timedelta
from test import slow_test
import os

def test_skip_slow_test():
    test_name = "test"
    now = slow_test._now()
    slow_test._set_timestamp(test_name, now - timedelta(seconds=2))

    assert slow_test._skip_test(test_name, timedelta(seconds=2)) == False
    assert slow_test._skip_test(test_name, timedelta(seconds=4)) == True

def test_slow():
    test_name = "test2"
    file_name = slow_test._get_filename(test_name)
    if os.path.isfile(file_name):
        os.remove(file_name)

    def get_skip():
        with slow_test.skip_slow_test(test_name, max_age=timedelta(seconds=60)) as skip:
            return skip

    assert get_skip() == False
    assert get_skip() == True
