#!/bin/bash

OLD_DS_NAME=MAPS
NEW_DS_NAME=MAPS_NEW

AUDIO_SUBDIR=AUDIO
MIDI_SUBDIR=MIDI
ANNOT_SUBDIR=ANNOTATION

function check_create_dir() {
    NEW_DIR=$1
    if ! [[ -d $NEW_DIR ]]
        then
        mkdir $NEW_DIR
    fi
}

function copy_filetype() {
    OLD_DIR=$1
    NEW_DIR=$2
    F_LIKE=$3

    echo "$NEW_DIR"
    find "$OLD_DIR" -name "$F_LIKE" -exec cp {} "$NEW_DIR" \;
}

check_create_dir "$NEW_DS_NAME"
check_create_dir "$NEW_DS_NAME"/"$AUDIO_SUBDIR"
check_create_dir "$NEW_DS_NAME"/"$MIDI_SUBDIR"
check_create_dir "$NEW_DS_NAME"/"$ANNOT_SUBDIR"

copy_filetype "$OLD_DS_NAME" "$NEW_DS_NAME"/"$MIDI_SUBDIR" "*.mid*"
copy_filetype "$OLD_DS_NAME" "$NEW_DS_NAME"/"$AUDIO_SUBDIR" "*.wav"
copy_filetype "$OLD_DS_NAME" "$NEW_DS_NAME"/"$ANNOT_SUBDIR" "*.txt"
