from openai import OpenAI
from playsound import playsound


def generate_audio_response(text: str, output_file_path: str = "speech.mp3") -> None:
    """
    Generate an audio response from the given text using OpenAI's text-to-speech service.

    Args:
        text (str): The text to be converted to speech.
        output_file_path (str): The path where the output audio file will be saved.
    """
    client = OpenAI()
    print('Reached 1---')
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )
    print('Reached 2---')

    response.stream_to_file(output_file_path)
    print('Reached 3---')

def play_sound(sound_path: str = "speech.mp3") -> None:
    """
    Play a sound file using the playsound module.

    Args:
        sound_path (str): The path to the sound file to be played.
    """
    print('Reached 4---')
    playsound(sound_path)
    print('Reached 5---')