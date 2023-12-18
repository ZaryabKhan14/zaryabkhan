from flask import Flask, request, render_template, Blueprint
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from io import BytesIO


imagegenerator_app = Blueprint('/imagegenerator',__name__)
# Initialize the Flask app


# Load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Route for the main page
@imagegenerator_app.route('/imagegenerator', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('prompt')
        image_url = generate_and_display_image(user_input)
        return render_template('imagegenerator.html', image_url=image_url)
    return render_template('imagegenerator.html', image_url=None)

# Function to generate and display the image
def generate_and_display_image(text, model="dall-e-3", size="1024x1024", quality="standard"):
    try:
        response = client.images.generate(
            model=model,
            prompt=text,
            size=size,
            quality=quality,
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


