import os
import sys
from difflib import SequenceMatcher

import speech_recognition as sr
from app.storage.client import StorageClient
from nltk import ngrams
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self):
        self.storage_client = StorageClient("http://localhost:5000")
        self.celeb_names = [
            name.lower() for name in self.storage_client.get_names()
        ]

    def run(self, filename):
        # Input audio file to be sliced
        audio = AudioSegment.from_wav(filename)

        # Length of the audiofile in milliseconds
        n = len(audio)

        # Variable to count the number of sliced chunks
        counter = 1

        # Text file to write the recognized audio
        fh = open("recognized.txt", "w+")

        interval = 3 * 1000
        overlap = 1.5 * 1000

        # Initialize start and end seconds to 0
        start = 0
        end = 0

        # Flag to keep track of end of file.
        # When audio reaches its end, flag is set to 1 and we break
        flag = 0

        mute_at = []
        # Iterate from 0 to end of the file,
        # with increment = interval
        for i in range(0, 2 * n, interval):

            # During first iteration,
            # start is 0, end is the interval
            if i == 0:
                start = 0
                end = interval

            # All other iterations,
            # start is the previous end - overlap
            # end becomes end + interval
            else:
                start = end - overlap
                end = start + interval

            # When end becomes greater than the file length,
            # end is set to the file length
            # flag is set to 1 to indicate break.
            if end >= n:
                end = n
                flag = 1

            # Storing audio file from the defined start to end
            chunk = audio[start:end]

            # Filename / Path to store the sliced audio
            chunk_filename = 'chunk' + str(counter) + '.wav'

            # Store the sliced audio file to the defined path
            chunk.export(chunk_filename, format="wav")
            # Print information about the current chunk
            print("Processing chunk " + str(counter) + ". Start = " +
                  str(start) + " end = " + str(end))

            # Increment counter for the next chunk
            counter = counter + 1

            # Slicing of the audio file is done.
            # Skip the below steps if there is some other usage
            # for the sliced audio files.

            # Here, Google Speech Recognition is used
            # to take each chunk and recognize the text in it.

            # Specify the audio file to recognize

            AUDIO_FILE = chunk_filename

            # Initialize the recognizer
            r = sr.Recognizer()

            # Traverse the audio file and listen to the audio
            with sr.AudioFile(AUDIO_FILE) as source:
                audio_listened = r.listen(source)

            # Try to recognize the listened audio
            # And catch expections.
            try:
                rec = r.recognize_google(audio_listened)
                recs = rec.split(' ')
                ngrms = list(ngrams(recs, 1)) + list(ngrams(recs, 2)) + list(
                    ngrams(recs, 3))
                ngrms = ['_'.join(ng) for ng in ngrms]

                result = []
                for ng in ngrms:
                    ng = ng.lower()
                    for celeb_name in self.celeb_names:
                        similarity = SequenceMatcher(a=ng,
                                                     b=celeb_name).ratio()
                        if similarity >= 0.8:
                            result.append(celeb_name)
                            break

                if len(result) > 0:
                    mute_at.append((start, end))

                text = f"START=[{start/1000}], END=[{end/1000}] | {ngrms}, {result}\n"
                print(text)
                fh.write(text)

            # If google could not understand the audio
            except sr.UnknownValueError:
                print("Could not understand audio")

            # If the results cannot be requested from Google.
            # Probably an internet connection error.
            except sr.RequestError as e:
                print("Could not request results.")

            os.remove(chunk_filename)

            # Check for flag.
            # If flag is 1, end of the whole audio reached.
            # Close the file and break.
            if flag == 1:
                fh.close()
                break

        if len(mute_at) == 0:
            AudioSegment.export(audio, 'out.wav')
            return

        merged_intervals = []
        left, right = mute_at[0]
        print(mute_at)
        for start, end in mute_at[1:]:
            if start > right:
                merged_intervals.append((left, right))
                left = start
                right = end
            else:
                right = end
        merged_intervals.append((left, right))

        # censor_audio = AudioSegment.from_wav('arcade.wav')
        print(merged_intervals)
        result_audio = AudioSegment.silent(0)
        cur = 0
        for start, end in merged_intervals:
            result_audio += audio[cur:start]
            result_audio += AudioSegment.silent(end - start)
            cur = end
        result_audio += audio[cur:]

        AudioSegment.export(result_audio, 'out.wav', format='wav')

        return [{
            "time_start": start / 1000,
            "time_end": end / 1000
        } for start, end in merged_intervals]

    @staticmethod
    def long_censor(censor_audio, duration):
        result = AudioSegment.silent(0)
        for _ in range(duration):
            result += censor_audio[:2]
        AudioSegment.export(result, 'long.wav', format='wav')
        return result


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 0

    proc = AudioProcessor()
    proc.run(filename)
