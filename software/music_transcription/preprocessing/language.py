from mido import MidiFile, bpm2tempo, tempo2bpm, second2tick
import sys
import numpy as np

# Full array printing
np.set_printoptions(threshold=sys.maxsize)


def get_tempo(tracks, default=500000):
    tempo = default
    for track in tracks:
        for x in track:
            try:
                tempo = x.tempo
            except AttributeError as e:
                pass
    return tempo


def get_timing(filename, frequency):
    mid = MidiFile(filename)
    tempo = get_tempo(mid.tracks)
    bpm = tempo2bpm(tempo)
    tpb = frequency * 60 / bpm
    print(f"bpm: {bpm}\tfreq: {frequency}\ttpb: {tpb}")
    return bpm, tpb


def get_fac(midi, target_length):
    length = second2tick(midi.length, midi.ticks_per_beat,
                         get_tempo(midi.tracks))
    fac = target_length / length
    # print(fac)
    return fac, length


def track2notes(track):
    notes = []
    cur_time = 0
    cur_notes = dict()
    for msg in track:
        cur_time += msg.time
        # adj_time = int(cur_time / tpb)
        if msg.type == "note_on" and msg.velocity != 0:
            cur_notes[msg.note] = cur_time
        elif msg.type == "note_off" or (msg.type == "note_on" and
                                        msg.velocity == 0):
            notes.append(
                {"note": msg.note, "on": cur_notes[msg.note], "off": cur_time})
            del cur_notes[msg.note]
    if cur_notes:
        print(f"WARNING! Some notes still pending after parsing: {cur_notes}")
    return notes


def notes2roll(notes, target_length, fac):
    roll = np.full((target_length, 88), False)
    for note in notes:
        if 21 <= note["note"] <= 108:
            # print(f"old: {note['on']} new:{int(note['on']*fac)}")
            roll[[range(int(note["on"]*fac), int(note["off"]*fac))],
                 [note['note']-21]] = True
    # print(roll)
    return roll

    '''
    roll = np.full((60, 12), False)
    # roll = np.put(roll, [[0, 3], [1, 3]], [True, True])
    roll[[range(5)], [1]] = True
    print(roll)
    '''


# def midi2roll(fname, freq=31.25):
#     bpm, tpb = get_timing(fname, freq)
def midi2roll(fname, target_length):
    mid = MidiFile(fname)
    fac, length = get_fac(mid, target_length)
    # print(f"length: {length}\t target_length: {target_length}\t fac: {fac}")
    for i, track in enumerate(mid.tracks):
        # print('Track {}: {}'.format(i, track.name))
        notes = track2notes(track)
        roll = notes2roll(notes, target_length, fac)
        return roll


def main():
    roll = midi2roll(sys.argv[1], 1000)
    print(roll)


if __name__ == '__main__':
    main()
