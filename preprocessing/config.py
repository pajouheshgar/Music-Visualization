import librosa


class Config:
    BINS_PER_OCTAVE = 12
    N_OCTAVES = 5
    N_BINS = N_OCTAVES * BINS_PER_OCTAVE
    F_MIN = librosa.note_to_hz('C1')
    HOP_LENGTH = 512
