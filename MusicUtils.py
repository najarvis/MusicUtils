from typing import Union

import random
import time

# Global notes list
NOTES = ["C/B#", "C#/Db", "D", "D#/Eb", "E/Fb", "F/E#", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B/Cb"]

# Intervals
p1 = 0 # Perfect unison
m2 = 1 # Minor second
M2 = 2 # Major second
m3 = 3 # Minor third
M3 = 4 # Major third
P4 = 5 # Perfect fourth
P5 = 7 # Perfect fifth
m6 = 8 # Minor sixth
M6 = 9 # Major sixth
m7 = 10 # Minor seventh
M7 = 11 # Major seventh
P8 = 12 # Perfect Octave

# Common scale intervals
major_scale = [M2, M2, m2, M2, M2, M2, m2]
minor_scale = [M2, m2, M2, M2, m2, M2, M2] # Notice how this is the same as the major scale, just starting on a different note
# Could be written as `minor_scale = major_scale[5:] + major_scale[:5]`
major_pentatonic_scale = [M2, M2, m3, M2, m3]
minor_pentatonic_scale = [m3, M2, M2, m3, M2] # Notice how this is the same as the major pentatonic scale, just starting on a different note
# Could be written as `minor_pentatonic_scale = major_pentatonic_scale[4:] + major_pentatonic_scale[:4]`

HEPATONIC_MODE_OFFSETS = {
    "ionian":      0,
    "dorian":     1,
    "phrygian":   2,
    "lydian":     3,
    "mixolydian": 4,
    "aeolian":    5,
    "locrian":    6
}

PENTATONIC_MODE_OFFSETS = {
    "P1": 0,
    "P2": 1,
    "P3": 2, # Note no P4 or P7, as those are the missing notes from the heptonic scale
    "P5": 3,
    "P6": 4
}

"""Given a starting note, list of intervals, and optional preference, print out the notes in a scale (always starting with the root)"""
def get_scale(starting_note: Union[str, int], scale: list, preference: str="") -> list:
    if type(starting_note) == str:
        index = find_note_index(starting_note)
        if index == -1:
            print("Invalid starting note.")
            return []

    elif type(starting_note) == int:
        index = starting_note

    else:
        print("Invalid starting note type.")
        return []

    arr = []
    for i in [0] + scale: # Always start on the root
        index += i
        note = NOTES[index % len(NOTES)]
        arr.append(get_preferred_note(note, preference))
    return arr

def get_formatted_scale(starting_note: Union[str, int], scale: list) -> list:
        # Since we don't want to display two of the same note names in the scale
        # (i.e C and C#), see if it makes more sense to display with sharps or flats.
        scale1 = get_scale(starting_note, scale, "#")
        scale2 = get_scale(starting_note, scale, "b")
        scale1_uniques = len(set(x[0] for x in scale1)) # Unique note names ("C#" and "C" both become C)
        scale2_uniques = len(set(x[0] for x in scale2))
        warning = len(scale) not in [scale1_uniques, scale2_uniques]
        if scale1_uniques >= scale2_uniques:
            return scale1, warning

        return scale2, warning

"""Given an entry in the NOTES list get a single note representation, with an optional preference for flat/sharp"""
def get_preferred_note(full_note: str, preference: str="") -> str:
        if preference == "#" and "#" in full_note:
            return full_note.split("/")[0]

        elif preference == "b" and "b" in full_note:
            return full_note.split("/")[1]

        else: 
            # Assume we always want to display the first note
            if "/" in full_note:
                return full_note.split("/")[0]

            return full_note

"""Given a note name find the index at which it can be found in the NOTES list"""
def find_note_index(note: str) -> int:
    for i in range(len(NOTES)):
        if note == NOTES[i]:
            return i

        if note in NOTES[i] and '/' in NOTES[i]:
            split_notes = NOTES[i].split('/')
            if note == split_notes[0] or note == split_notes[1]:
                return i
    
    return -1

"""Print out a visual representation of a string with a given number of frets. """
def print_string(starting_note: str, frets: int, preference: str="") -> None:
    index = find_note_index(starting_note)
    if index == -1:
        return

    for i in range(frets):
        note = NOTES[(index + i) % len(NOTES)]
        p_note = get_preferred_note(note, preference)
        disp_note = p_note + "-" if len(p_note) == 1 else p_note
        print(disp_note, end='')
        if i < (frets - 1):
            print("-|", end='')
        else:
            print()

"""Print out the fret numbers in the same format as the strings from print_string"""
def print_string_indicies(frets: int) -> None:
    for i in range(frets):
        end = '-' * (4 - len(str(i))) if i < (frets - 1) else '\n'
        print(i, end=end)

"""Print a visual representation of the entire neck with a given number of frets."""
def print_neck(strings: Union[list, str], frets: int, preference: str="", reverse: bool=True, indicies: bool=True) -> None:
    # Reverse is just an easier way to print the strings with high on the top
    order = strings[::-1] if reverse else strings

    if indicies:
        print_string_indicies(frets)

    for starting_note in order:
        print_string(starting_note, 16, preference)
    print()

"""Print only the notes on the neck that are part of a given scale. This function has a lot of duplicated code. TODO: Clean up"""
def print_scale_neck(starting_note: Union[int, str], scale: list, strings: Union[list, str], frets: int, preference: str="", reverse: bool=True, indicies: bool=True) -> None:
    scale_notes = get_scale(starting_note, scale, preference)
    order = strings[::-1] if reverse else strings

    if indicies:
        print_string_indicies(frets)

    for starting_note in order:
        index = find_note_index(starting_note)
        if index == -1:
            return

        for i in range(frets):
            note = NOTES[(index + i) % len(NOTES)]
            p_note = get_preferred_note(note, preference)
            disp_note = p_note + "-" if len(p_note) == 1 else p_note
            if p_note in scale_notes:
                print(disp_note, end='')
            else:
                print("--", end='')
            if i < (frets - 1):
                print("-|", end='')
            else:
                print()
    print()

"""For a given string and fret, return the letter name of the note."""
def get_note_at_fret(string, fret):
    index = find_note_index(string)
    note = NOTES[(index + fret) % len(NOTES)]
    # print("The note on string {} at fret {} is {}".format(string, fret, note))
    return note

def mode_quiz(pentatonic = False):
    base_scale = major_scale if not pentatonic else major_pentatonic_scale
    choice = "X"
    while choice != "":
        offsets = HEPATONIC_MODE_OFFSETS if not pentatonic else PENTATONIC_MODE_OFFSETS
        random_mode = random.choice(list(offsets.keys()))
        random_mode_num = offsets[random_mode]
        mode_intervals = base_scale[random_mode_num:] + base_scale[:random_mode_num]

        scale, warning = get_formatted_scale("C", mode_intervals)

        print("What mode is: ")
        print(scale)
        if warning: # If the number of unique notes in the shown scale are not the same as the number of notes in the base scale, we know it is not a valid written scale
            print("Warning: Possibly not a valid scale/mode")
        choice = input()
        print("It was: {}".format(random_mode))

"""Basic quiz, which asks about notes at a random fret on a random string."""
def quiz(bass_mode = True):
    strings = "EADG" if bass_mode else "EADGBE"
    max_fret = 20
    while True:
        random_string = random.choice(strings)
        random_fret = random.randint(0, max_fret)
        test_note = get_note_at_fret(random_string, random_fret)
        print("What is the note at fret {} on the {} string?".format(random_fret, random_string))
        input_note = input(": ")
        if input_note == "0":
            break

        split_notes = test_note.split('/')
        if input_note in split_notes or input_note == test_note:
            print("Correct!")
        else:
            #print(split_notes)
            print("Incorrect, the correct answer was {}".format(test_note))

"""Exercise for learning the notes on the fretboard."""
def note_finder():
    while True:
        t0 = time.time()
        note = random.choice(NOTES)
        disp_note = get_preferred_note(note, random.choice("#b"))
        directions = [
            "highest to lowest",
            "lowest to highest",
            "on the E string",
            "on the A string",
            "on the D string",
            "on the G string"
        ]
        print("Find everywhere the note {} appears, {}".format(disp_note, random.choice(directions)))
        user_input = input()
        if user_input == "0":
            break

        print("Elapsed: {}s".format(time.time()-t0))
        
def menu():
    print("Would you like to do the (Q)uiz, (M)ode test, or (N)ote Finder?")
    while (choice := input(": ").upper()) not in "QNM" and choice != "":
        print("That is not an option")

    if choice == "Q":
        quiz(False)
    
    elif choice == "M":
        mode_quiz()

    elif choice == "N":
        note_finder()
    
    print("Goodbye!")

if __name__ == "__main__":
    print("C Major scale")
    print(get_scale("C", major_scale))

    print("C Minor scale")
    print(get_scale("C", minor_scale, "b"))

    print("C Major pentatonic scale")
    print(get_scale("C", major_pentatonic_scale))

    print("C Minor pentatonic scale")
    print(get_scale(0, minor_pentatonic_scale, "b")) # Works to put the index in there as well

    print("Standard bass fretboard (16 frets)")
    print_neck("EADG", 16)

    print("G minor pentatonic notes on the fretboard")
    print_scale_neck("G", minor_pentatonic_scale, "EADG", 16, "b")

    menu()

    # get_scale("A", minor_scale, "b") # Try it out with any starting note / scale