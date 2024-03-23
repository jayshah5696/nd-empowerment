from flask import Flask, render_template, request
from flask_cors import CORS
import dotenv
import os
from pydantic import BaseModel, validator
from pathlib import PosixPath
import bentoml
# load dot env file
# Load the .env file
dotenv.load_dotenv('.env')


app = Flask(__name__)
CORS(app)  # Enable CORS for the entire application

def generateImage():
    # This function will be responsible for generating the image
    # For now, it does nothing
    pass

@app.route('/explain', methods=['GET', 'POST'])
def explain():
    if request.method == 'POST':
        # Handle the POST request for the 'explain' endpoint
        data = request.form
        # Perform the necessary operations based on the received data
        return 'Explanation generated'
    return render_template('explain.html')

@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    if request.method == 'POST':
        # Handle the POST request for the 'visualize' endpoint
        data = request.form
        # Call the generateImage function
        generateImage()
        # Return the string representing the image path
        return "/Users/aghatage/Documents/code/nde/logo.png"
    return render_template('visualize.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'POST':
        # Handle the POST request for the 'read' endpoint
        data = request.form
        # Perform the necessary operations based on the received data
        return 'Reading performed'
    return render_template('read.html')

# Access the environment variables
tts_api = os.getenv('tts_id')


class SynthesizeInput(BaseModel):
    lang: str
    text: str

class SynthesizeOutput(BaseModel):
    result: PosixPath

    @validator('result', pre=True)
    def convert_to_posixpath(cls, v):
        return PosixPath(v)

def synthesize_text(input_data: SynthesizeInput) -> SynthesizeOutput:
    with bentoml.SyncHTTPClient(tts_api) as client:
        result = client.synthesize(
            lang=input_data.lang,
            text=input_data.text,
        )
    return SynthesizeOutput(result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
