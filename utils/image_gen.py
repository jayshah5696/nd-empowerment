import requests
import dotenv
import os
import base64
from PIL import Image
import uuid
import io
dotenv.load_dotenv('.env')
firworks_api_key = os.getenv("FIREWORKS_API_KEY")
def generate_image(prompt, get_b64=False):
    url = "https://api.fireworks.ai/inference/v1/image_generation/accounts/fireworks/models/stable-diffusion-xl-1024-v1-0"

    payload = {
        "height": 1024,
        "width": 1024,
        "text_prompts": [
            {
                "weight": 1,
                "text": prompt
            }
        ],
        "cfg_scale": 7,
        "samples": 1,
        "seed": 0,
        "steps": 50,
        "safety_check": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {firworks_api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    base64_image = response.json()[0]['base64']
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))
    # filename_generation using uuid
    uuid_value = uuid.uuid4()
    filename = f"{uuid_value}.png"
    image.save(filename)
    if get_b64:
        return filename, base64_image
    else:
        return filename

# Usage
# response = generate_image("hill with greenary")
# from IPython.display import Image, display
# import base64

# base64_image = response.json()[0]['base64']
# image_bytes = base64.b64decode(base64_image)
# display(Image(image_bytes))

# from PIL import Image

# # Save the image locally
# image = Image(image_bytes)
# image.save("image.png")