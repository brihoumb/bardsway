import os
import sys
import random

import wandb
import pickle
import logging
import numpy as np
import pandas as pd
from keras.utils import plot_model
from wandb.keras import WandbCallback
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model
from keras.optimizers import SGD, Adam, Adadelta
from keras.layers import Dense, Conv2D, Conv1D, Flatten,\
                         MaxPool2D, Reshape, Dropout, MaxPool1D

from software.src.options import get_field
from music_transcription.utils import check_create_dir, f1_m
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

    def __load_dataset(self):
        print("Loading dataset...")
        self.dataset = pd.read_pickle(self.dataset_fpath)
        print(f"Model loaded with X_shape = {self.dataset['X'].shape}," +
              "y_shape = {self.dataset['y'].shape}")

    def __get_model_window(self):
        print("Loading model...")
        # -- input shape : ((batch_size,) height, width, depth)

        input_shape = self.dataset["X"].shape[1:]
        print(input_shape)
        model = Sequential()

        model.add(Conv2D(25, (5, 25), activation="relu",
                         padding="same", input_shape=input_shape))
        model.add(MaxPool2D((1, 3)))
        model.add(Dropout(0.5))

        model.add(Conv2D(100, (3, 5), padding="same", activation="relu"))
        model.add(MaxPool2D((2, 1)))
        model.add(Dropout(0.5))

        model.add(Flatten())
        model.add(Dense(1000, activation="sigmoid"))
        model.add(Dropout(0.5))
        model.add(Dense(88, activation="softmax"))

        model.summary()

        optimizers = {"Adadelta": Adadelta(learning_rate=self.params["l_rate"],
                                           rho=0.95, epsilon=1e-7),
                      "SGD": SGD(learning_rate=self.params["l_rate"],
                                 momentum=0.9),
                      "Adam": Adam(learning_rate=self.params["l_rate"])}

        model.compile(loss=self.params["loss"],
                      optimizer=optimizers[self.params["optimizer"]],
                      metrics=["acc"])
        self.model = model

    def prepare_training(self, dataset_fpath, optimizer, loss, l_rate=1e-2):
        self.dataset_fpath = dataset_fpath
        self.params["optimizer"] = optimizer
        self.params["loss"] = loss
        self.params["l_rate"] = l_rate
        self.__load_dataset()
        self.__get_model_window()
        if self.wandb_export:
            wandb.init(project="music-transcription")

    def train(self, epochs, batch_size=256):
        if not self.model or not self.dataset:
            return -1
        self.params["epochs"] = epochs
        self.params["batch_size"] = batch_size
        checkpoint = ModelCheckpoint(self.model_path,
                                     monitor="val_acc",
                                     verbose=1, mode="max",
                                     save_best_only=True,
                                     save_weights_only=False, period=1)

        if self.wandb_export:
            wandb.config.update(self.params)
            callbacks = [checkpoint, WandbCallback()]
        else:
            callbacks = [checkpoint]

        self.model.fit(self.dataset['X'],
                       self.dataset['y'],
                       epochs=epochs,
                       batch_size=batch_size,
                       shuffle=True,
                       validation_split=0.2,
                       callbacks=callbacks)

        self.model.save(self.model_path)
        t = self.__compute_threshold()
        self.__export_threshold(t)

    def __export_threshold(self, threshold, t_output="threshold.p"):
        with open(t_output, 'wb') as handle:
            pickle.dump(threshold, handle, protocol=4)

    def __import_threshold(self, t_input="threshold.p"):
        with open(t_input, 'rb') as handle:
            self.threshold = pickle.load(handle)

    def __import_model(self):
        logging.info('-$- Importing model... -$-')
        self.model = load_model(self.model_path)

    def __compute_threshold(self):
        if not self.dataset:
            self.__load_dataset()
        y_pred = self.model.predict(self.dataset["X"])
        logging.info("-$- Computing threshold... -$-")

        best = {"t": 0, "f": 0}
        for t in np.linspace(0, 1, 10000, endpoint=False):
            bins = np.where(y_pred > t, 1, 0)
            f = f1_m(self.dataset["y"], bins).numpy()
            if f > best["f"]:
                best = {"t": t, "f": f}
        return best["t"]

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


def main():
    dataset_fpath = os.path.join("preprocessing", "data.p")
    tm = TranscriptionModel(wandb_export=False)
    tm.prepare_training(dataset_fpath,
                        optimizer="SGD", loss="binary_crossentropy",
                        l_rate=1e-2)

    # tm.train(epochs=1, batch_size=256)
    tm.predict()


if __name__ == '__main__':
    main()
