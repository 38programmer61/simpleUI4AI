import base64
import os
import time

import pandas as pd
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import streamlit as st
# import numpy as np
# import time
from st_audiorec import st_audiorec
# from langchain.llms import OpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

from audio_input import convert_audio_to_text
from audio_output import generate_audio_response, play_sound
from image_output import generate_a_single_image
from image_input import generate_caption
from send_message_to_ai import send_message_to_ai, execute_prompt
from PIL import Image
import io
from pydub import AudioSegment

start_time=-2



def main():
    load_dotenv()
    chain, chat_history = initialize_chatbot()
    initialize_sessions_state()
    prepare_components(chain, chat_history)
    run_app(chain, chat_history)

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
    chat_history = ChatMessageHistory()

    return chain, chat_history

def initialize_sessions_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def prepare_components(chain, chat_history):
    prepare_sidebar_components()
    prepare_main_components(chain, chat_history)

def prepare_main_components(chain, chat_history):
    # Main components
    st.title('IAMAI')
    if st.session_state["audio_input"]:
        wav_audio_data = st_audiorec()
        st.session_state.wav_audio_data = wav_audio_data

        # if wav_audio_data is not None and len(wav_audio_data) > 5e5:
        #     print('Valid')
        #     # print(type(wav_audio_data))
        #     with open("recording.mp3", "wb") as f:
        #         f.write(wav_audio_data)
        #     prompt = convert_audio_to_text()
        #     execute_prompt(chain, chat_history, prompt)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # if st.session_state["img_file_input"]:
    #     st.session_state.conversation.append(st.session_state["img_file_input"])
    # for img in st.session_state.conversation:
    #     st.image(img)
        # st.image(st.session_state["img_file_input"])
    # st.write(st.session_state["audio_input"])
    # st.write(st.session_state["audio_output"])
    # st.write(st.session_state["prompt"])

def prepare_sidebar_components():
    # Sidebar components
    st.sidebar.title("I/O and Settings")
    st.sidebar.image("Image.png", width=250)
    st.sidebar.button("Start A New Conversation", key="conv")
    audio_input = st.sidebar.checkbox("Auditory Input", key="audio_input")
    if st.session_state["audio_input"]:
        audio_send = st.sidebar.button('Send Recorded Audio', key="talk")
    audio_output = st.sidebar.checkbox("Auditory Output", key="audio_output")
    prompt = st.sidebar.text_input(label="Your Command", key="prompt")
    text_button = st.sidebar.button("Send Text ", key="text_submit")
    img_file_input = st.sidebar.file_uploader("Image Input", key="img_file_input")
    img_button = st.sidebar.button("Send Image", key="img_send")
    # cam_inp = st.sidebar.camera_input(label="cam_inp", key="cam_inp")
    # wav_audio_data = st_audiorec()
    #
    # if wav_audio_data is not None:
    #     st.audio(wav_audio_data, format='audio/wav')

def run_app(chain, chat_history):

    # prompt = st.session_state["prompt"]
    if st.session_state["conv"]:
        st.session_state.messages = []

    if st.session_state["text_submit"]:
        prompt = st.session_state["prompt"]
        execute_prompt(chain, prompt)

    if st.session_state["audio_input"] and st.session_state["talk"]:
    # if st.session_state["talk"]:
        if st.session_state.wav_audio_data is not None and len(st.session_state.wav_audio_data) > 5e4:
            global start_time
            start_time = time.time()
            print('Valid')
            # print(type(wav_audio_data))



            # --- previous version ---
            # with open("recording.mp3", "wb") as f:
            #     f.write(st.session_state.wav_audio_data)

            with open("output.wav", "wb") as f:
                f.write(st.session_state.wav_audio_data)



            audio = AudioSegment.from_wav("output.wav")
            audio.export("recording.mp3", format="mp3", parameters=["-ac","2","-ar","8000"])
            # print("1) Before  convert_audio_to_text: --- %s seconds ---" % (time.time() - start_time))
            prompt = convert_audio_to_text()
            # print("2) Before  execute_prompt: --- %s seconds ---" % (time.time() - start_time))
            execute_prompt(chain, prompt)


    if st.session_state["img_send"]:
        with st.chat_message("user"):
            st.image(st.session_state["img_file_input"])
            st.session_state.messages.append({"role": "user", "content": "image"})
            # print(type(st.session_state["img_file_input"].getvalue()))
            byte_data = st.session_state["img_file_input"].getvalue()
            byte_stream = io.BytesIO(byte_data)
            image = Image.open(byte_stream)
            image.save('img_to_caption.png')
            caption = generate_caption('img_to_caption.png')
            # caption = generate_caption()

        if st.session_state["audio_output"]:
            # start_time = time.time()
            generate_audio_response(caption)
            # print("4) AI response obtained: --- %s seconds ---" % (time.time() - start_time))
            with st.chat_message("assistant"):
                st.markdown(caption)
            # print("5) End: --- %s seconds ---" % (time.time() - start_time))
            play_sound()

        else:
            with st.chat_message("assistant"):
                st.markdown(caption)
        # with st.chat_message("assistant"):
        #     st.markdown(caption)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": caption})




if __name__ == '__main__':
    main()