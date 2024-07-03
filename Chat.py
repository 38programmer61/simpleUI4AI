from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import streamlit as st
from st_audiorec import st_audiorec
from langchain_community.chat_message_histories import ChatMessageHistory
from audio_input import convert_audio_to_text
from audio_output import generate_audio_response, play_sound
from image_input import generate_caption
from send_message_to_ai import execute_prompt
from PIL import Image
import io
from pydub import AudioSegment

def main():
    load_dotenv()
    chain = initialize_chatbot()
    initialize_sessions_state()
    prepare_components()
    run_app(chain)

def initialize_chatbot():
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | chat

    return chain

def initialize_sessions_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def prepare_components():
    prepare_sidebar_components()
    prepare_main_components()

def prepare_main_components():
    st.title('IAMAI')
    if st.session_state["audio_input"]:
        wav_audio_data = st_audiorec()
        st.session_state.wav_audio_data = wav_audio_data

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def prepare_sidebar_components():
    st.sidebar.title("I/O and Settings")
    st.sidebar.image("Image.png", width=250)
    st.sidebar.button("Start A New Conversation", key="conv")
    st.sidebar.checkbox("Auditory Input", key="audio_input")
    if st.session_state["audio_input"]:
        st.sidebar.button('Send Recorded Audio', key="talk")
    st.sidebar.checkbox("Auditory Output", key="audio_output")
    st.sidebar.text_input(label="Your Command", key="prompt")
    st.sidebar.button("Send Text ", key="text_submit")
    st.sidebar.file_uploader("Image Input", key="img_file_input")
    st.sidebar.button("Send Image", key="img_send")


def run_app(chain):

    if st.session_state["conv"]:
        st.session_state.messages = []

    if st.session_state["text_submit"]:
        prompt = st.session_state["prompt"]
        execute_prompt(chain, prompt)

    if st.session_state["audio_input"] and st.session_state["talk"]:
        if st.session_state.wav_audio_data is not None and len(st.session_state.wav_audio_data) > 5e4:

            with open("output.wav", "wb") as f:
                f.write(st.session_state.wav_audio_data)

            audio = AudioSegment.from_wav("output.wav")
            audio.export("recording.mp3", format="mp3", parameters=["-ac","2","-ar","8000"])
            prompt = convert_audio_to_text()
            execute_prompt(chain, prompt)

    if st.session_state["img_send"]:
        with st.chat_message("user"):
            st.image(st.session_state["img_file_input"])
            st.session_state.messages.append({"role": "user", "content": "image"})
            byte_data = st.session_state["img_file_input"].getvalue()
            byte_stream = io.BytesIO(byte_data)
            image = Image.open(byte_stream)
            image.save('img_to_caption.png')
            caption = generate_caption('img_to_caption.png')

        if st.session_state["audio_output"]:
            generate_audio_response(caption)
            with st.chat_message("assistant"):
                st.markdown(caption)
            play_sound()

        else:
            with st.chat_message("assistant"):
                st.markdown(caption)

        st.session_state.messages.append({"role": "assistant", "content": caption})

if __name__ == '__main__':
    main()