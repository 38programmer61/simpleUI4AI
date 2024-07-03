from pathlib import Path
from openai import OpenAI
from playsound import playsound

def generate_audio_response(response):

    client = OpenAI()

    speech_file_path = "./speech.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice="fable",
      input=response
    )

    response.stream_to_file(speech_file_path)


def play_response():
    playsound("speech.mp3")