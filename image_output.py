import os
import requests
import base64
from typing import Dict, Any

def generate_a_single_image(prompt: str) -> None:
    """
    Generate a single image based on a text prompt and save it.

    Args:
        prompt (str): The text prompt to generate the image from.
    """
    data = make_api_call_to_sdxl(prompt)
    save_image(data)

def make_api_call_to_sdxl(prompt: str) -> Dict[str, Any]:
    """
    Make an API call to the Stable Diffusion XL engine to generate an image.

    Args:
        prompt (str): The text prompt to generate the image from.

    Returns:
        Dict[str, Any]: The response data containing the generated image artifacts.

    Raises:
        Exception: If the API key is missing or the response status is not 200.
    """
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
        raise Exception(f"Non-200 response: {response.text}")

    return response.json()

def save_image(data: Dict[str, Any], image_path_and_name: str = "image") -> None:
    """
    Save the generated image from the response data to a file.

    Args:
        data (Dict[str, Any]): The response data containing the generated image artifacts.
        image_path_and_name (str): The base name for the saved image file.
    """
    for i, image in enumerate(data["artifacts"]):
        with open(f"{image_path_and_name}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))
