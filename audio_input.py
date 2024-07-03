import time
import warnings

from openai import OpenAI

def convert_audio_to_text():
    # start_time = time.time()
    # warnings.filterwarnings('ignore')
    # client = OpenAI()
    #
    # audio_file = open("recording.mp3", "rb")
    # transcription = client.audio.transcriptions.create(
    #     model="whisper-1",
    #     file=audio_file
    # )
    # print("--- %s seconds ---" % (time.time() - start_time))
    # return transcription.text


    warnings.filterwarnings('ignore')
    client = OpenAI()

    audio_file = open("recording.mp3", "rb")


    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text