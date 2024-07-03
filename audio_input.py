import streamlit as st
from openai import OpenAI
from pydub import AudioSegment
from send_message_to_ai import execute_prompt


def convert_audio_to_text(audio_file_path: str = "recording.mp3") -> str:
    """
    Convert audio file to text using OpenAI's transcription service.

    Args:
        audio_file_path (str): The path to the audio file to transcribe.

    Returns:
        str: The transcribed text from the audio file.
    """
    client = OpenAI()

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    return transcription.text

def process_audio_input(chain) -> None:
    """
    Process audio input and send the prompt to the chatbot.

    Args:
        chain: The chatbot chain.
    """
    if st.session_state.wav_audio_data is not None and len(st.session_state.wav_audio_data) > 5e4:
        with open("output.wav", "wb") as f:
            f.write(st.session_state.wav_audio_data)

        audio = AudioSegment.from_wav("output.wav")
        audio.export("recording.mp3", format="mp3", parameters=["-ac", "2", "-ar", "8000"])
        prompt = convert_audio_to_text("recording.mp3")
        execute_prompt(chain, prompt)

