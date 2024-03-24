from flask import Flask, request
from flask_cors import CORS
import os
from pydantic import BaseModel, validator
from pathlib import PosixPath
import bentoml
import dotenv
import json

# Load the .env file
dotenv.load_dotenv('.env')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from all origins

# Function to generate image (placeholder)
def generateImage(user_input):
    # This function will be responsible for generating the image
    # For now, it does nothing
    print(user_input)
    pass

# Endpoint for explaining text
@app.route('/explain', methods=['POST'])
def explain():
    data = request.form
    # Perform the necessary operations based on the received data
    return 'Explanation generated'

# Endpoint for visualizing text
@app.route('/visualize', methods=['POST'])
def visualize():
    print('Received input:', request.json)
    text = request.json.get('text', '')
    generateImage(text)
    # Return the image URL
    return "file:///Users/aghatage/Documents/code/nde/logo.png"

# Endpoint for reading text
@app.route('/read', methods=['POST'])
def read():
    data = request.form
    print('Called READ, sending to Synthesize output')
    input_data = SynthesizeInput(lang='en', text=data['text'])
    print('Got Synthesize output')
    result = synthesize_text(input_data)
    print('Synthesize output: ' + result.result)
    # Perform the necessary operations based on the received data
    return result.result

# Access the environment variables
tts_api = os.getenv('tts_id')

# Define input and output models
class SynthesizeInput(BaseModel):
    lang: str
    text: str

class SynthesizeOutput(BaseModel):
    result: PosixPath

    @validator('result', pre=True)
    def convert_to_posixpath(cls, v):
        return PosixPath(v)

# Function to synthesize text using TTS API
def synthesize_text(input_data: SynthesizeInput) -> SynthesizeOutput:
    with bentoml.SyncHTTPClient(tts_api) as client:
        result = client.synthesize(
            lang=input_data.lang,
            text=input_data.text,
        )
    return SynthesizeOutput(result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

