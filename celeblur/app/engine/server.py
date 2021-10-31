import json
import multiprocessing
import os
import subprocess

from flask import Flask, request

from audio import AudioProcessor
from video import VideoProcessor

global audio_processor
audio_processor = AudioProcessor()

global video_processor
video_processor = VideoProcessor()

global manager
manager = multiprocessing.Manager()

app = Flask(__name__)

# def process_video(source, proc_num, return_dict):
#     return_dict[proc_num] = video_processor.run(source)


def process_video(source):
    return video_processor.run(source)


def process_audio(source):
    return audio_processor.run(source)


@app.route("/recognize", methods=["POST"])
def emb_add():
    data = request.get_json(force=True)
    source = data["source"]

    audio_filename = "audio.wav"
    command = f"echo yes | ffmpeg -i {source} -ac 1 -ar 16000 -vn {audio_filename}"
    subprocess.call(command, shell=True)

    # return_dict = manager.dict()
    # p = multiprocessing.Process(target=process_video, args=(source, 0, return_dict))
    # p.start()

    video_timecodes = process_video(source)
    audio_timecodes = process_audio(audio_filename)
    # p.join()

    # video_timecodes = return_dict[0]

    with open(f"{prefix}_video.json", 'w') as f:
        json.dump({"result": video_timecodes}, f)

    with open(f"{prefix}_audio.json", 'w') as f:
        json.dump({"result": audio_timecodes}, f)

    return Response(
        json.dumps({
            "audio": audio_timecodes,
            "video": video_timecodes
        }),
        status=200
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ["PORT"]))
