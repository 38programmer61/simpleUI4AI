from openai import OpenAI

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
