import streamlit as st
from audio_output import generate_audio_response, play_sound
from image_output import generate_a_single_image


def send_message_to_ai(chain) -> str:
    """
    Send messages to the AI model and get a response.

    Args:
        chain: The AI model chain to interact with.

    Returns:
        str: The AI response content.
    """
    response = chain.invoke({"messages": st.session_state.messages})
    return response.content


def execute_prompt(chain, prompt: str) -> None:
    """
    Execute a given prompt by either generating an image or sending the message to the AI model.

    Args:
        chain: The AI model chain to interact with.
        prompt (str): The user's prompt to execute.
    """
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "draw" in prompt.lower() or "çiz" in prompt.lower():
        generate_image_from_prompt(prompt)
    else:
        handle_text_response(chain, prompt)


def generate_image_from_prompt(prompt: str) -> None:
    """
    Generate an image based on the given prompt.

    Args:
        prompt (str): The user's prompt to generate an image from.
    """
    if "draw" in prompt.lower():
        image_prompt = prompt[4:]
    else:  # for "çiz"
        image_prompt = prompt[:-3]

    generate_a_single_image(image_prompt)
    with st.chat_message("assistant"):
        st.image("image.png")
    st.session_state.messages.append({"role": "assistant", "content": "Image Generated"})


def handle_text_response(chain, prompt: str) -> None:
    """
    Handle the text response from the AI model.

    Args:
        chain: The AI model chain to interact with.
        prompt (str): The user's prompt to send to the AI model.
    """
    response = send_message_to_ai(chain)
    if st.session_state.get("audio_output", False):
        generate_audio_response(response)
        with st.chat_message("assistant"):
            st.markdown(response)
        play_sound()
    else:
        with st.chat_message("assistant"):
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
