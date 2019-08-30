import itertools
import os
import json
import numpy as np

# pylint: disable=inconsistent-return-statements
def get_new_filename(filename_template):
    for i in itertools.count():
        filename = filename_template.format(i)
        if not os.path.isfile(filename):
            return filename


def write_test_data(description, data):
    class NumpyEncoder(json.JSONEncoder):
        # pylint: disable=method-hidden
        def default(self, o):
            if isinstance(o, np.ndarray):
                return o.tolist()
            return json.JSONEncoder.default(self, o)

    filename = get_new_filename(f"test/{description}_{{0:03d}}.json")
    with open(filename, "w") as file:
        json.dump(data, file, cls=NumpyEncoder)

    print(f"Written to {filename}")
