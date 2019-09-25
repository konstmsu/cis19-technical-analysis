#!./venv/bin/python

import pprint
import zipfile
import os
import app.generation


def generate_files():
    directory = "static"
    if not os.path.exists(directory):
        os.makedirs(directory)

    seeds = range(100, 1000)
    zip_filename = os.path.join(directory, "sample_data.zip")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(
            "README.TXT",
            "Sample training data for Technical Analysis challenge of CodeIT Suisse 2019",
        )

        print(f"Writing '{zip_file.filename}'", end="")
        for seed in seeds:
            scenarios = app.generation.get_standard_scenarios(seed)
            data = pprint.pformat(
                [s.train_signal.tolist() for s in scenarios], compact=True
            )
            filename = f"TA_{seed}.json"
            zip_file.writestr(filename, data)
            print(".", end="", flush=True)

    print(f"written {len(seeds)} json files")


if __name__ == "__main__":
    generate_files()
