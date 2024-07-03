# The following resources were useful
# - https://platform.stability.ai/docs/api-reference#tag/Text-to-Image

import os
import requests
import base64

def generate_a_single_image(prompt):
    data = make_api_call(prompt)
    save_image(data)

def make_api_call(prompt):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "height": 1024,
            "width": 1024,
            "samples": 1,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    return data

def save_image(data):
    image_path_and_name = "image"
    for i, image in enumerate(data["artifacts"]):
        with open(image_path_and_name + ".png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))
