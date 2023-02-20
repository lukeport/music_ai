#Make a pop song


import os
import time

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

number_of_chords = 30
number_of_files = 1

parts = ['Chords', 'Bass', 'Melody']

chord_choice_weights = [0.3, 0.025, 0.025, 0.2, 0.3, 0.15, 0, 0]



#############################################################################################################
#               Model/Generator

#Files loop
for file in list(range(number_of_files)):
    #creates an empty score for each file 
    score = stream.Score()    
    
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
    #define voices
    chord_part = stream.Part()
    bass_part = stream.Part()
    melody_part = stream.Part()
    
    
    #making chord voice
    for chord_num in list(range(number_of_chords + 1)):
        # Define the root note
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
        
        
        #making bass part
        bass_note_pitch = root_note_pitch
        bass_note = note.Note(bass_note_pitch)
        bass_note.octave = 1
        bass_note.duration = duration.Duration(chord_duration)
        bass_part.append(bass_note)

                
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
        
        
    #generating melody
    melody_length = 0
    max_melody_length = chord_duration * number_of_chords
    
    
    while melody_length < max_melody_length:
        
        #get scale
        scale = score_key.getScale()
        
        #choose melody note
        melody_pitch = random.choice(scale.pitches)
        melody_note = note.Note(melody_pitch)
        
        #selects note duration
        
        
        rand_float = random.uniform(0, 4)
        float_interval = 0.1
        rand_float = round(rand_float / float_interval) * float_interval            
        melody_note.quarterLength = rand_float
        
        #selects melody note pitch
        melody_note.octave = random.randint(4, 7)
        
        melody_length += rand_float
        melody_part.append(melody_note)
    
    
        
    
    
    
    
    #inserting parts into score
    score.insert(0, chord_part)
    score.insert(0, bass_part)
    score.insert(0, melody_part)

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
    
    #write score to musical notation pdf
    
    
    end_time = time.time()

    print("Time taken:", end_time - start_time, "seconds")
    
    print(f'file {file + 1} printed')
    score.show('text')

print("Time taken:", end_time - start_time, "seconds")


