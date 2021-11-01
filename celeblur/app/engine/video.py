import sys
import time

import cv2
import face_recognition
import numpy as np
from app.storage.client import StorageClient
from face_recognition.api import face_locations

SCALE = 2
MIN_TIME_FOR_DETECTION = 1000
UNKNOWN_NAME = "Unknown"
BLUR_RADIUS = 91
NUM_SKIP_FRAMES = 6
DETECTION_THRESHOLD = 0.5



class VideoProcessor:
    def __init__(self):
        self.storage_client = StorageClient("http://storage:5000")

    def run(self, cap_from):
        cap = cv2.VideoCapture(cap_from)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter("/opt/out_tmp.mp4", fourcc, cap.get(cv2.CAP_PROP_FPS),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        frame_counter = 0
        timecodes = []
        cur_dets = {}
        while cap.isOpened():
            ret, img = cap.read()

            if not ret:
                break

            if frame_counter < NUM_SKIP_FRAMES:
                frame_counter += 1
                continue

            frame_counter = 0

            t_cur = cap.get(cv2.CAP_PROP_POS_MSEC)
            print(t_cur / 1000)

            # Resize frame of video to 1/4 size for faster face recognition processing

            face_locations, face_names = self.detect_faces(img)
            self.update_curent_detections(cur_dets, face_names, t_cur, timecodes)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= SCALE
                right *= SCALE
                bottom *= SCALE
                left *= SCALE

                if name != UNKNOWN_NAME:
                    img[top:bottom, left:right] = cv2.GaussianBlur(
                        img[top:bottom, left:right],
                        (BLUR_RADIUS, BLUR_RADIUS), 0)

                    if name not in cur_dets:
                        cur_dets[name] = (t_cur, [bottom, left], [top, right])

                # Draw a box around the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left, bottom), (right, bottom), (0, 0, 255), cv2.FILLED)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # cv2.imshow('result', img)
            for _ in range(NUM_SKIP_FRAMES+1):
                out.write(img)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        out.release()
        return timecodes

    def detect_faces(self, img):
        small_frame = cv2.resize(img, (0, 0), fx=1 / SCALE, fy=1 / SCALE)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = self.storage_client.emb_find_match(face_encoding, DETECTION_THRESHOLD)

            face_names.append(name)

        return face_locations, face_names

    def update_curent_detections(self, cur_dets, face_names, t_cur, timecodes):
        for name in list(cur_dets.keys()):
            if name in face_names:
                continue

            t_start, [x1, y1], [x2, y2] = cur_dets[name]
            if t_cur - t_start < MIN_TIME_FOR_DETECTION:
                continue

            print(f"{name}: START=[{t_start}], END=[{t_cur}]")
            timecodes.append({
                "time_start": t_start,
                "time_end": t_cur,
                "corner_1": [x2, y2],
                "corner_2": [x1, y1],
            })

            del cur_dets[name]


if __name__ == "__main__":
    cap_from = sys.argv[1] if len(sys.argv) > 1 else 0

    proc = VideoProcessor()
    proc.run(cap_from)
