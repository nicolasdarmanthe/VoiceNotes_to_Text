#https://deepspeech.readthedocs.io/en/

#Import required packages
from deepspeech import Model
import numpy as np
import os
import wave
import subprocess


class BootUp():
    """
    Class for importing DeepSpeech model files, and set some basic parameters
    """
    def __init__(self, model_file_path, lm_file_path, beam_width, lm_alpha, lm_beta):
        self.model_file_path = model_file_path
        self.lm_file_path = lm_file_path
        self.beam_width = beam_width #lower number for faster inference
        self.lm_alpha = lm_alpha #optimal params
        self.lm_beta = lm_beta

    def model_construct(self):
        self.model = Model(self.model_file_path)
        self.model.enableExternalScorer(self.lm_file_path)
        self.model.setScorerAlphaBeta (self.lm_alpha, self.lm_beta)
        self.model.setBeamWidth(self.beam_width)
        return self.model

#Move this to main?
bootup = BootUp("deepspeech-0.9.3-models.pbmm","deepspeech-0.9.3-models.scorer",800,0.93,1.18)
model = bootup.model_construct()

#class FileConcat():
#    """
#    Class for concatenating multiple audio files together. Can detect recordings taken close in time and automatically concatenate them together.
#    """
#    def __init__(self,ffmpegloc,autoconcat,manualconcatlist=None):
#        self.ffmpegloc = ffmpegloc
#        self.autoconcat = autoconcat
#        self.manualconcatlist = manualconcatlist
#    def concatenate_files(self):
#        if self.autoconcat == "yes":
#            #do stuff to find files that are recorded close in time
#        else:
#            #concatthelist provided manually

class FileConverter():
    """
    Class for converting video or sound files into the appropriate format (sound must be 16k Hz)
    """
    def __init__(self,ffmpegloc, filetoconvert,newfilename):
        self.ffmpegloc = ffmpegloc
        self.filetoconvert = filetoconvert
        self.newfilename = newfilename

    def convert_file(self):
        os.system(self.ffmpegloc + ' -i ' + self.filetoconvert + ' -ar 16000 ' + self.newfilename)

#Testing the file converter
fileconverter = FileConverter("C:/Users/nicol/Local_Documents/VoiceNotes_to_Text/ffmpeg/bin/ffmpeg.exe","C:/Users/nicol/Local_Documents/VoiceNotes_to_Text/SoundFiles/210112_0017.WMA","C:/Users/nicol/Local_Documents/VoiceNotes_to_Text/SoundFiles/latest.wav")
fileconverter.convert_file()

class FileProperties():
    """
    Class for reading audio file to transcribe.
    """
    def __init__(self,filename):
        self.filename = filename

    def read_wav_file_properties(self):
        with wave.open(self.filename, 'rb') as w:
            self.rate = w.getframerate()
            self.frames = w.getnframes()
            self.buffer = w.readframes(self.frames)
            #print(self.frames)
            #print(self.rate)

        return self

#This is just for interest, to show what the class does
fileproperties = FileProperties("SoundFiles/test.wav")
filepropertiesdata = fileproperties.read_wav_file_properties()

class FileTranscriber():
    """
    Class for transcribing audio to text.
    """
    def __init__(self,audiofile):
        self.audiofile = audiofile

    def transcribe(self):
        self.fileproperties = FileProperties(self.audiofile) #make us of read_wav_file_properties method in FileProperties class
        self.filepropertiesdata = self.fileproperties.read_wav_file_properties()

        self.buffer, self.rate = self.fileproperties.buffer, self.fileproperties.rate
        self.data16 = np.frombuffer(self.buffer, dtype=np.int16)
        
        return model.stt(self.data16)

#Run the transcriber method
filetranscriber = FileTranscriber("SoundFiles/latest.wav")
transcribedtext = filetranscriber.transcribe()

print(transcribedtext)