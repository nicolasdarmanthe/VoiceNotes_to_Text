#https://deepspeech.readthedocs.io/en/

from deepspeech import Model
import numpy as np
import os
import wave

model_file_path = "deepspeech-0.9.3-models.pbmm"
lm_file_path = "deepspeech-0.9.3-models.scorer"
beam_width = 800 #lower number for faster inference
lm_alpha = 0.93 #optimal params
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)

model.setScorerAlphaBeta (lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        print(rate)
        print(frames)

    return buffer, rate

def transcribe(audio_file):
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)
