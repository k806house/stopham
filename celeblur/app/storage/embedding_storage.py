import os
import pickle

import face_recognition
import numpy as np


class EmbeddingStorage:
    def __init__(self):
        self.encodings = []
        self.names = []

    def add(self, encoding, name):
        self.encodings.append(encoding)
        self.names.append(name)

    def find_match(self, encoding, tol=0.6):
        name = "Unknown"
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(self.encodings,
                                                 np.array(encoding), tol)

        if True in matches:
            first_match_index = matches.index(True)
            name = self.names[first_match_index]

        return name

    def save(self, filename):
        pickle.dump(self.index, filename)

    def load(self, filename):
        if os.path.exists(filename):
            self.index = pickle.load(filename)
