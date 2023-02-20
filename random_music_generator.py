


import os
import time

start_time = time.time()

from music21 import *
import random

os.chdir('C:\\Users\March\OneDrive\Documents\music AI app')

#############################################################################################################
#               Functions





#############################################################################################################
#               Lists
note_list = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
US_note_durations = ['whole', 'half']

possible_key_list = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 
                 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 
                 'B']
major_minor_list = ['major', 'minor']


time_signatures = ['4/4', '3/4']
#############################################################################################################
#                       Inputs
max_notes_per_voice = 30
voice_num = 10
number_files = 1



#############################################################################################################
#               Model/Generator

#Files loop
for file in list(range(number_files)):
    #creates an empty score for each file 
    score = stream.Score()    
    #choose a key signature, based on random number of sharps or flats
    score_key = key.Key(possible_key_list[random.randint(0, len(possible_key_list) - 1)],
                        major_minor_list[random.randint(0, 1)])
    score.insert(0, score_key)
    
    #make list of notes in key to select from
    pitch_list = score_key.pitches
    
    #choose a time signature
    score_time_signature = meter.TimeSignature(time_signatures[random.randint(0,1)])
    score.insert(0, score_time_signature)
    
    #voice loop
    for voice in list(range(voice_num)):
        #creates empty part for each voice
        temp_part = stream.Part()
        #note loop
        for x in list(range(max_notes_per_voice)):
            
            #select note
            n = pitch_list[random.randint(0, len(pitch_list) - 1)]
            n = note.Note(n)
            
            #selects note duration
            rand_float = random.uniform(0, 4)
            interval = 0.1
            rand_float = round(rand_float / interval) * interval            
            n.quarterLength = rand_float
            
            #selects note octave
            n.octave = random.randint(3, 8)
            
            #appends note to voice
            temp_part.append(n)
        
        score.insert(0, temp_part)
    # Write the stream to a MIDI file        
    mf = midi.translate.music21ObjectToMidiFile(score)
    
    #assign score key to variable
    analysed_key = score.analyze('key')
    #assign score time signature to variable
    analysed_time_signature = score.timeSignature.ratioString
    file_time_sig = analysed_time_signature.replace('/', '_')
    #write score to midi
    mf.open(f"random_songs\key_{analysed_key}_time_sig_{file_time_sig}.mid", "wb")
    mf.write()
    mf.close()
    
    #write score to musical notation pdf
    
    
    end_time = time.time()

    print("Time taken:", end_time - start_time, "seconds")
    
    print(f'file {file + 1} printed')

print("Time taken to generate all files:", end_time - start_time, "seconds")




