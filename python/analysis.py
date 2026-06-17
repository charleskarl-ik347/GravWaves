import numpy as np
from scipy.signal import chirp

def generate_gravitational_wave_like_signal(
    sample_rate: int = 512,
    duration: float = 2.0,
    start_freq: float = 30.0,
    end_freq: float = 180.0,
    noise_level: float = 0.35,
):
    # generate a random signal. Not official data cos f conda envs

    n = int(sample_rate * duration)
    time = np.linspace(0, duration, n, endpoint=False)

    clean_signal = chirp(
        time,
        f0=start_freq,
        f1=end_freq,
        t1=duration,
        method="quadratic",
    )

    # Growing amplitude envelope, just merger in terms opf simplicity
    envelope = np.exp(2.8 * (time - duration))
    clean_signal = clean_signal * envelope

    noise = noise_level * np.random.normal(size=n)
    raw_signal = clean_signal + noise

    return time, raw_signal, clean_signal


def run_fourier_analysis(
    sample_rate: int = 512,
    duration: float = 2.0,
    low_cut: float = 25.0,
    high_cut: float = 220.0,
):
    #fft, inversefft, and filtering of the signal

    time, raw_signal, clean_signal = generate_gravitational_wave_like_signal(
        sample_rate=sample_rate,
        duration=duration,
    )

    fft_values = np.fft.rfft(raw_signal)
    frequencies = np.fft.rfftfreq(len(raw_signal), d=1 / sample_rate)
    magnitude = np.abs(fft_values)

    filtered_fft = fft_values.copy()
    filtered_fft[(frequencies < low_cut) | (frequencies > high_cut)] = 0

    reconstructed_signal = np.fft.irfft(filtered_fft, n=len(raw_signal))

    return {
        "time": time.tolist(),
        "raw_signal": raw_signal.tolist(),
        "clean_signal": clean_signal.tolist(),
        "frequencies": frequencies.tolist(),
        "magnitude": magnitude.tolist(),
        "reconstructed_signal": reconstructed_signal.tolist(),
        "low_cut": low_cut,
        "high_cut": high_cut,
        "sample_rate": sample_rate,
        "duration": duration,
    }