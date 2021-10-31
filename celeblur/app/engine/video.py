import sys
import time

import cv2
import face_recognition
import numpy as np
from app.storage.client import StorageClient

SCALE_DOWN = 2

class Watcher:
    def __init__(self):
        self.storage_client = StorageClient("http://localhost:5000")

    def run(self, cap_from):
        cap = cv2.VideoCapture(cap_from)

        flag = True
        while cap.isOpened():
            ret, img = cap.read()

            if not ret:
                break

            if flag:
                flag = not flag
                continue

            # Resize frame of video to 1/4 size for faster face recognition processing

            small_frame = cv2.resize(img, (0, 0), fx=1/SCALE_DOWN, fy=1/SCALE_DOWN)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                name = self.storage_client.emb_find_match(face_encoding, 0.5)

                face_names.append(name)

            for (top, right, bottom,
                 left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= SCALE_DOWN
                right *= SCALE_DOWN
                bottom *= SCALE_DOWN
                left *= SCALE_DOWN

                top -= 150
                bottom += 50

                if name != "Unknown":
                    img[top:bottom, left:right] = cv2.GaussianBlur(
                        img[top:bottom, left:right], (91, 91), 0)

                # Draw a box around the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255),
                              2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left, bottom - 35), (right, bottom),
                              (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0,
                            (255, 255, 255), 1)

            cv2.imshow('result', img)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()


if __name__ == "__main__":
    cap_from = sys.argv[1] if len(sys.argv) > 1 else 0

    watcher = Watcher()
    watcher.run(cap_from)
