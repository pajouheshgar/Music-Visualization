import numpy as np
import librosa
import matplotlib.pyplot as plt

import scipy.io.wavfile as wavfile
import scipy.stats

from preprocessing.config import Config


def extract_bar_cqt(sr, wav_data):
    """
    :param sr: Sample Rate of the Wav file
    :param wav_data: Single Channel Wav Data
    :return: splits of wav_data into bars by finding tempo dynamically
    """
    onset_env = librosa.onset.onset_strength(y=wav_data, sr=sr)
    prior = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr, hop_length=Config.HOP_LENGTH, prior=prior)
    beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
    times = librosa.times_like(pulse, sr=sr)
    frequencies = librosa.cqt_frequencies(n_bins=Config.N_BINS, fmin=Config.F_MIN,
                                          bins_per_octave=Config.BINS_PER_OCTAVE)
    cqt = np.abs(
        librosa.cqt(wav_data, sr=sr, fmin=Config.F_MIN, n_bins=Config.N_BINS, bins_per_octave=Config.BINS_PER_OCTAVE))
    cqt_db = librosa.amplitude_to_db(cqt, ref=np.max)
    cqt_split = []
    for i, b in enumerate(beats_plp[:-1]):
        cqt_split.append(cqt_db[:, b: beats_plp[i + 1]])

    cqt_split.append(cqt_db[:, beats_plp[-1]:])
    return cqt_split, times[beats_plp]


if __name__ == '__main__':
    sr, wav_data = wavfile.read("../dataset/wav/SanTropez.wav")
    wav_data = np.mean(wav_data, axis=1)

    cqt_split, times = extract_bar_cqt(sr, wav_data)
    print(len(cqt_split))
    print(len(times))
    print(cqt_split[100].shape)
    print(cqt_split[200].shape)
    for i in range(450):
        print(cqt_split[i][17].mean())
    f = range(60)
    plt.plot(f, np.mean(cqt_split[100], axis=-1))
    plt.show()
