import io
import os
import time
import pyperclip
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from audio_output import generate_audio_response, play_sound
from PIL import Image


def generate_caption(img_path: str = "img_to_caption.png") -> str:
    """
    Generate a caption for an image using Pallyy's image description generator.

    Args:
        img_path (str): The path to the image file to generate a caption for.

    Returns:
        str: The generated caption or an error message if the process fails.
    """
    try:
        img_full_path = os.path.join(os.getcwd(), img_path)

        # Set up Chrome options to handle browser configuration
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

        # Open the image description generator page
        driver.get("https://pallyy.com/tools/image-description-generator")
        time.sleep(3)  # Allow time for the page to load

        # Upload the image file
        upload = driver.find_element(By.TAG_NAME, 'input')
        upload.send_keys(img_full_path)
        time.sleep(25)  # Allow time for the image to be processed

        # Click the generate button
        hit_button = driver.find_element(By.CLASS_NAME, 'generate-button')
        hit_button.click()
        time.sleep(5)  # Allow time for the caption to be generated

        # Click the clipboard copy button
        clipboard_copy_button = driver.find_elements(By.CLASS_NAME, 'tweet__button-copy')[1]
        clipboard_copy_button.click()
        time.sleep(5)  # Allow time for the caption to be copied to the clipboard

        # Retrieve the caption from the clipboard
        res_str = pyperclip.paste()

        # Close the browser
        driver.quit()

        return res_str
    except Exception as e:
        return "I'm tired, please try it later."


def process_image_input() -> None:
    """
    Process image input and generate a caption.

    Args:
        chain: The chatbot chain.
    """
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
