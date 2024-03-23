from flask import Flask, render_template, request
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
