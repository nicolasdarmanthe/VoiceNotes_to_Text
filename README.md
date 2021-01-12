# VoiceNotes_to_Text
This app does some audio file processing and ultimately converts voice to formatted text.

NOTES:

#Need to convert files into wav, with freq 16k Hz
C:\Users\nicol\Local_Documents\VoiceNotes_to_Text\ffmpeg\bin\ffmpeg.exe -i Soundfiles\210111_0001.WMA -ar 16000 SoundFiles\test2.wav

#Concatenating files
#First, create list.txt file with the files to concatenate. Then run -
C:\Users\nicol\Local_Documents\VoiceNotes_to_Text\ffmpeg\bin\ffmpeg.exe -f concat -i list.txt -c copy SoundFiles/merged.wav