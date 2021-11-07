import numpy as np
import pickle
from midiutil.MidiFile import MIDIFile


def find_duration(tab, note, x):
    duration = 0
    while x < len(tab) and tab[x][note] == 1:
        duration += 1
        x += 1
    return duration


def add_note_to_midi(tab, note, data, mf):
    pitch = 21 + note
    x = 0
    while x < len(tab):
        if tab[x][note] == 1:
            time = x
            duration = find_duration(tab, note, x)
            x += duration
            mf.addNote(data["track"], data["channel"], pitch,
                       time / 15.625, duration / 15.625, data["volume"])
        else:
            x += 1


def roll2midi(tab, tempo=120, output="out.mid"):
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track
    time = 0    # start at the beginning
    mf.addTrackName(track, time, output)
    mf.addTempo(track, time, tempo)
    channel = 0
    volume = 100
    data = {"track": track, "channel": channel, "volume": volume}

    note = 0
    while note < len(tab[0]):
        add_note_to_midi(tab, note, data, mf)
        note += 1

    with open(output, 'wb') as outf:
        mf.writeFile(outf)


def main():
    with open('roll_test.p', 'rb') as handle:
        tab = pickle.load(handle)
    # print(tab)
    roll2midi(tab, 120, "test.mid")


if __name__ == "__main__":
    main()
