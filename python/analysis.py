import numpy as np

from gwosc import load_wave_file


def run_fourier_analysis(
    filename,
    low_cut=25.0,
    high_cut=220.0,
):
    wave = load_wave_file(filename)

    time = wave["time"]
    raw_signal = wave["strain"]
    sample_rate = wave["sample_rate"]
    duration = wave["duration"]

    fft_values = np.fft.rfft(raw_signal)

    frequencies = np.fft.rfftfreq(
        len(raw_signal),
        d=1 / sample_rate
    )

    magnitude = np.abs(fft_values)

    filtered_fft = fft_values.copy()

    filtered_fft[
        (frequencies < low_cut)
        |
        (frequencies > high_cut)
    ] = 0

    reconstructed_signal = np.fft.irfft(
        filtered_fft,
        n=len(raw_signal)
    )

    return {
        "filename": wave["filename"],
        "time": time.tolist(),
        "raw_signal": raw_signal.tolist(),
        "frequencies": frequencies.tolist(),
        "magnitude": magnitude.tolist(),
        "reconstructed_signal": reconstructed_signal.tolist(),
        "low_cut": low_cut,
        "high_cut": high_cut,
        "sample_rate": sample_rate,
        "duration": duration,
        "gps_start": wave["gps_start"],
    }