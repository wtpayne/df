import io
import os
import requests
from PIL import Image
import openai



def save_image( image_data, filename):
    image = Image.open(io.BytesIO(image_data))
    image.save(filename)

def download_image( url):
    response = requests.get(url)
    return response.content

def generate_image_tool( input):
    prompt = f"{input}"
    response = openai.Image.create(
        prompt=prompt,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    image = download_image(image_url)

    if not os.path.exists("images"):
        os.mkdir("images")
    img_files = os.listdir("images")
    img_count = len(img_files)
    img_file_name = f"image_{img_count}.png"
    img_path = os.path.join("images", img_file_name)
    save_image(image, img_path)

    return img_path