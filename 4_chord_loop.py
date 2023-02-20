#Make a pop song


import os
import time
import numpy as np
start_time = time.time()

from music21 import *
import random
import fluidsynth
import wave

print('Modules loaded.')
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

major_intervals = [interval.Interval(4), interval.Interval(7)]
minor_intervals = [interval.Interval(3), interval.Interval(7)]
diminshed_intervals = [interval.Interval(4), interval.Interval(6)]
#############################################################################################################
#                       Inputs


number_of_files = 1
chords_per_loop = 4
loop_repetitions = 10

parts = ['Chords', 'Bass', 'Melody']

chord_choice_weights = [0.35, 0, 0, 0.3, 0.2, 0.15, 0, 0]
note_choice_weights = [0.3, 0.05, 0.05, 0.2, 0.2, 0.15, 0.05, 0]


#############################################################################################################
#               Model/Generator

#create empty score
score = stream.Score()    

#Create empty streams for chords and melody
chord_part = stream.Part()
melody_part = stream.Part()

#choose a key signature, based on random number of sharps or flats
key_string = possible_key_list[random.randint(0, len(possible_key_list) - 1)]
print(key_string)

#make key pitch for if loop
key_pitch = pitch.Pitch(f'{key_string}4')

#insert key
score_key = key.Key(key_string)
score.insert(0, score_key)

#make list of notes in key to select from
pitch_list = score_key.pitches  

#choose a time signature
score_time_signature = meter.TimeSignature(time_signatures[random.randint(0,1)])
score.insert(0, score_time_signature)

#making the 4 chord loop 
for chord_ in list(range(chords_per_loop)):
    
    root_note_pitch = random.choices(pitch_list, weights=chord_choice_weights)[0]
    root_note = note.Note(root_note_pitch)

    #chord duration
    chord_duration = 4
        
    #determine nature of chord
    semitones_diff = root_note_pitch.ps - key_pitch.ps
    semintone_diff_remainder = semitones_diff % 8
      
    if semintone_diff_remainder == 1 or semintone_diff_remainder == 2 or semintone_diff_remainder == 6:
        chord_intervals = minor_intervals
    elif semintone_diff_remainder == 0 or semintone_diff_remainder == 4 or semintone_diff_remainder == 5:
        chord_intervals = major_intervals
    else:
        chord_intervals = diminshed_intervals
                
    #set root note octave        
    root_note.octave = random.randint(3, 5)

    # Generate the chord
    temp_chord = chord.Chord([root_note])
    for interval_ in chord_intervals:
        temp_chord.add(root_note.transpose(interval_))
        
    #chord duration
    chord_duration = 4
    temp_chord.duration = duration.Duration(chord_duration)
        
    # Append chord
    chord_part.append(temp_chord)
    print(f'Chord {chord_ + 1} done')

chord_loop = stream.Score()
chord_loop.repeatAppend(chord_part, loop_repetitions)


#generating melody
melody_length = 0
max_melody_length = chord_duration * loop_repetitions * chords_per_loop

#get scale
scale = score_key.getScale()

while melody_length < max_melody_length:
    
    #choose melody note
    melody_pitch = random.choices(scale.pitches, weights=note_choice_weights)[0]
    melody_note = note.Note(melody_pitch)
    
    #selects note duration
    
    
    rand_float = random.uniform(0, 4)
    float_interval = 0.1
    rand_float = round(rand_float / float_interval) * float_interval            
    melody_note.quarterLength = rand_float
    
    #selects melody note pitch
    melody_note.octave = random.randint(5, 6)
    
    melody_length += rand_float
    melody_part.append(melody_note)


    
score.insert(0, melody_part)
score.insert(0, chord_loop)
# Write the stream to a MIDI file        
mf = midi.translate.music21ObjectToMidiFile(score)

#assign score key to variable
analysed_key = score.analyze('key')
#assign score time signature to variable
analysed_time_signature = score.timeSignature.ratioString
file_time_sig = analysed_time_signature.replace('/', '_')
#write score to midi
mf.open(f"generated midi\key_{analysed_key}_time_sig_{file_time_sig}.mid", "wb")
mf.write()
mf.close()




score.show('text')
