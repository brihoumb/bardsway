import os
import sys
import shutil
import logging

from music_transcription import download
from gui.src.options import get_field
from music_transcription.model import TranscriptionModel


def entrypoint(*argv):
    dir = os.path.join(get_field("result"), 'to_pred_audio')
    if not os.path.exists(dir):
        os.makedirs(dir)
    if len(argv) >= 2:
        shutil.copyfile(argv[1], os.path.join(dir, 'piano.wav'))
    if not os.path.exists(get_field("rdn")):
        logging.critical("-$- Couldn't find music transcription model. -$-")
        return(84)
    if not os.path.exists(os.path.join(os.path.dirname(get_field("rdn")),
                                       'threshold.p')):
        logging.critical("-$- Couldn't find threshold file. -$-")
        return(84)
    tm = TranscriptionModel(model_path=get_field("rdn"),
                            wandb_export=False)
    tm.predict(audio_dir=os.path.join(get_field("result"), 'to_pred_audio'),
               feat_path=os.path.join(os.path.dirname(get_field("rdn")),
                                      'to_pred.p'),
               path=os.path.dirname(get_field("rdn")),
               music_name=argv[2])


if __name__ == '__main__':
    entrypoint(sys.argv)
