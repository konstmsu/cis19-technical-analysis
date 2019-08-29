import itertools
import os
import json
import numpy as np


def get_new_filename(filename_template):
    for i in itertools.count():
        filename = filename_template.format(i)
        if not os.path.isfile(filename):
            return filename


def write_test_data(description, data):
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):  # pylint: disable=method-hidden
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    filename = get_new_filename(f"test/{description}_{{0:03d}}.json")
    with open(filename, "w") as f:
        json.dump(data, f, cls=NumpyEncoder)

    print(f"Written to {filename}")
