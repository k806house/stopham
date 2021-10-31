import os
import pickle

import face_recognition
import numpy as np


class Storage:
    def __init__(self):
        self.encodings = []
        self.names = []

    def add(self, encoding, name):
        self.encodings.append(encoding)
        self.names.append(name)

    def find_match(self, encoding, tol=0.6):
        name = "Unknown"
        matches = face_recognition.compare_faces(self.encodings,
                                                 np.array(encoding), tol)

        face_distances = face_recognition.face_distance(
            self.encodings, np.array(encoding))
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = self.names[best_match_index]

        return name

    def get_names(self):
        return self.names

    def save(self, filename):
        with open(f"{filename}_encodings", 'wb') as pickle_file:
            pickle.dump(self.encodings, pickle_file)

        with open(f"{filename}_names", 'wb') as pickle_file:
            pickle.dump(self.names, pickle_file)

    def load(self, filename):
        with open(f"{filename}_encodings", 'rb') as pickle_file:
            self.encodings = pickle.load(pickle_file)

        with open(f"{filename}_names", 'rb') as pickle_file:
            self.names = pickle.load(pickle_file)
