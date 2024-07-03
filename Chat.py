import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from st_audiorec import st_audiorec
from audio_input import process_audio_input
from image_input import process_image_input
from send_message_to_ai import execute_prompt

def main() -> None:
    """
    Main function to initialize and run the Streamlit app.
    """
    load_dotenv()
    chain = initialize_chatbot()
    initialize_session_state()
    prepare_components()
    run_app(chain)

def initialize_chatbot() -> tuple:
    """
    Initialize the chatbot with OpenAI's model and the chat history.

    Returns:
        tuple: The chatbot chain and chat history.
    """
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | chat
    return chain

def initialize_session_state() -> None:
    """
    Initialize the session state for Streamlit.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

def prepare_components() -> None:
    """
    Prepare the components for the Streamlit app.

    Args:
        chain: The chatbot chain.
        chat_history: The chat history.
    """
    prepare_sidebar_components()
    prepare_main_components()

def prepare_main_components() -> None:
    """
    Prepare the main components of the Streamlit app.

    Args:
        chain: The chatbot chain.
        chat_history: The chat history.
    """
    st.title('IAMAI')
    if st.session_state["audio_input"]:
        wav_audio_data = st_audiorec()
        st.session_state.wav_audio_data = wav_audio_data

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def prepare_sidebar_components() -> None:
    """
    Prepare the sidebar components for the Streamlit app.
    """
    st.sidebar.title("I/O and Settings")
    st.sidebar.image("Image.png", width=250)
    st.sidebar.button("Start A New Conversation", key="conv")
    st.sidebar.checkbox("Auditory Input", key="audio_input")
    if st.session_state["audio_input"]:
        st.sidebar.button('Send Recorded Audio', key="talk")
    st.sidebar.checkbox("Auditory Output", key="audio_output")
    st.sidebar.text_input(label="Your Command", key="prompt")
    st.sidebar.button("Send Text", key="text_submit")
    st.sidebar.file_uploader("Image Input", key="img_file_input")
    st.sidebar.button("Send Image", key="img_send")

def run_app(chain) -> None:
    """
    Run the Streamlit app.

    Args:
        chain: The chatbot chain.
    """
    if st.session_state["conv"]:
        st.session_state.messages = []

    if st.session_state["text_submit"]:
        prompt = st.session_state["prompt"]
        execute_prompt(chain, prompt)

    if st.session_state["audio_input"] and st.session_state["talk"]:
        process_audio_input(chain)

    if st.session_state["img_send"]:
        process_image_input()


if __name__ == '__main__':
    main()
