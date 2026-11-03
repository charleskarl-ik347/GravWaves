from pathlib import Path

import h5py
import numpy as np


DATA_DIRECTORY = Path(__file__).parent / "data"


def list_wave_files():
    DATA_DIRECTORY.mkdir(exist_ok=True)

    return sorted(
        path.name
        for path in DATA_DIRECTORY.glob("*.hdf5")
    )


def load_wave_file(filename):
    file_path = DATA_DIRECTORY / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Wave file does not exist: {filename}"
        )

    with h5py.File(file_path, "r") as hdf_file:
        strain_dataset = hdf_file["strain"]["Strain"]

        strain = strain_dataset[:]

        dt = float(
            strain_dataset.attrs.get(
                "Xspacing",
                1 / 4096
            )
        )

        gps_start = float(
            strain_dataset.attrs.get(
                "Xstart",
                0
            )
        )

    sample_rate = 1 / dt
    duration = len(strain) * dt

    time = np.arange(len(strain)) * dt

    return {
        "filename": filename,
        "strain": strain,
        "time": time,
        "dt": dt,
        "gps_start": gps_start,
        "sample_rate": sample_rate,
        "duration": duration,
    }