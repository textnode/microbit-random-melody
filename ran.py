import random

one_octave = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B")

notes = []
for fill_octave in range(1,9):
    for note in one_octave:
        notes.append(note + str(fill_octave))
print(notes)

major_scale = (0, 2, 4, 5, 7, 9, 11)
minor_scale = (0, 2, 3, 5, 7, 8, 10)
minor_pentatonic_scale = (0,3,5,7,10)
harmonic_minor_scale = (0, 2, 3, 5, 7, 9, 10)

scales = (major_scale, minor_scale, minor_pentatonic_scale, harmonic_minor_scale)

def generate(root, scale, octave, bars, seed):
#    from enum import Enum
#    class note_range_option(Enum):
#        exclude_octave = 1
#        include_octave = 2
#        extend_above = 3
#        extend_below = 4
#        extend_above_and_below = 5

    offset = one_octave.index(root)

    available_notes_all_octaves = []
    done = False
    index_multiplier = 0
    while(not done):
        index_multiplier += 1
        for index in scale:
            place = offset + index + (len(one_octave) * (index_multiplier-1))
            print("%s = %s + %s + (%s * %s-1)" % (place, offset, index, len(one_octave), index_multiplier))
            if len(notes) > place:
                print("Adding note: %s" % notes[place])
                available_notes_all_octaves.append(notes[place])
            else:
                done = True

    print("Available notes all octaves: %s" % available_notes_all_octaves)
    print("Start on: %s, end on: %s" % (root + str(octave), root + str(octave+1)))
    available_notes_start = available_notes_all_octaves.index(root + str(octave))
    available_notes_end = available_notes_all_octaves.index(root + str(octave+1))
    available_notes_this_octave = available_notes_all_octaves[available_notes_start:available_notes_end+1]

    print("available notes on this octave: %s" % str(available_notes_this_octave))

    random.seed(seed)
    chosen_notes = []
    for bar in range(bars):
        slots = 4*4
        while slots > 0:
            note = available_notes_this_octave[random.randint(0, len(available_notes_this_octave)-1)]
            duration = random.randint(1, 4)
            if duration <= slots:
                chosen_notes.append(note + ":" + str(duration))
                slots -= duration
            else:
                chosen_notes.append("R:" + str(slots))
                slots -= slots

    print("Chosen notes: %s" % chosen_notes)
    return chosen_notes


def run():
    import math
    import microbit
    import music
    import time
    import speech

    music.set_tempo(ticks=4, bpm=60)
    microbit.compass.calibrate()

    score = []
    scale_index = 0
    scale = scales[scale_index]

    octave = 4

    while(True):
        gesture = microbit.accelerometer.current_gesture()
        if gesture == "face up":
            #speech.say("face up")
            octave = 4
        elif gesture == "left":
            #speech.say("left")
            octave = 3
        elif gesture == "right":
            #speech.say("right")
            octave = 5

        if microbit.pin_logo.is_touched():
            scale_index += 1
            scale_index = scale_index % len(scales)
            scale = scales[scale_index]
            microbit.display.show(scale_index)
            print("Scale: %s" % str(scale))
            time.sleep_ms(200)

        if microbit.button_a.is_pressed():
            heading = microbit.compass.heading()
            seed = math.floor(heading / 30)
            microbit.display.show(seed)
            score = generate("C", scale, octave, 1, seed)

        if microbit.button_b.is_pressed():
            music.play(score)

