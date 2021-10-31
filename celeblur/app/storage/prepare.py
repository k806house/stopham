import os
import glob
import random
import face_recognition
from client import StorageClient

dataset = glob.glob("unzippedFaces/*")
client = StorageClient("http://localhost:5000")

for celeb_dir in dataset:
    print(celeb_dir)
    celeb_name = celeb_dir.split('/')[-1]
    sessions = glob.glob(f"{celeb_dir}/*/*")
    sessions = random.sample(sessions, min(2, len(sessions)))
    sess_photos = [glob.glob(f"{sess}/*") for sess in sessions]
    sess_photos = [random.sample(photos, min(2, len(photos))) for photos in sess_photos]

    for photos in sess_photos:
        for img_path in photos:
            img = face_recognition.load_image_file(img_path)
            try:
                enc = face_recognition.face_encodings(img)[0]
                client.emb_add(enc, celeb_name)
            except:
                pass
