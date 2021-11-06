import os

import pickle
import logging
import numpy as np
from keras.models import load_model

from gui.src.options import get_field
from music_transcription.postprocessing.postprocess import roll2midi
from music_transcription.preprocessing.preprocess import preprocess_audio


class TranscriptionModel:
    def __init__(self, model_path="mt.model", wandb_export=False):
        self.model_path = model_path
        self.wandb_export = wandb_export
        self.dataset_fpath = None
        self.model = None
        self.dataset = None
        self.threshold = None
        self.params = {}

    def __import_threshold(self, t_input="threshold.p"):
        with open(t_input, 'rb') as handle:
            self.threshold = pickle.load(handle)

    def __import_model(self):
        logging.info('-$- Importing model... -$-')
        self.model = load_model(self.model_path)

    def predict(self, audio_dir="to_pred_audio",
                feat_path="to_pred.p", path='.', music_name=''):
        preprocess_audio(audio_dir, output=feat_path)
        self.__import_model()
        logging.info("-$- Loading threshold... -$-")
        self.__import_threshold(os.path.join(path, 'threshold.p'))
        logging.info("-$- Loading features... -$-")
        with open(feat_path, "rb") as handle:
            X = pickle.load(handle)
        if X is None:
            logging.error("-$- Loading failed. Exiting -$-")
            return -1
        logging.info("-$- Making prediction... -$-")
        y_pred = self.model.predict(X)
        logging.info("-$- Applying threshold... -$-")
        y_pred = np.where(y_pred > self.threshold, 1, 0)
        roll2midi(y_pred, output=os.path.join(get_field("result"), music_name,
                                              'piano.mid'))
        logging.info("-$- Midi file successfuly generated ! -$-")
