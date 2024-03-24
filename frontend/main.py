import os
from PIL import Image
import streamlit as st
import requests

# Function to make POST request to Flask API
def post_question_api(data):
    url = "http://localhost:5000/api/question"  # Change URL accordingly
    # response = requests.post(url, json=data)
    # return response.json()
    data = {
            "question":  "what do you like",
            "question_type": "like",
            "option_list": [
                            {"Image": "sample1.jpg", "Text_input": "sample1"},
                            {"Image": "sample2.jpg", "Text_input": "sample2"}
                            ],
            "done": False
        }
    return data

# Main Streamlit app
def main():
    # Function to render options
    def render_options(question, question_type, done, option_list, image_folder):
        for option in option_list:
            text_input = option.get("Text_input", "")
            image_file = option.get("Image", "")
            image_path = os.path.join(image_folder, image_file)
            data = {"Like": [], "Dislike": [], "Done": done}
            if os.path.exists(image_path):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(text_input):
                        if question_type.lower() == "like":
                            data['Like'].append({'Question': question, 'Answer': text_input})
                            post_question_api(data)
                        else:
                            data['DisLike'].append({'Question': question, 'Answer': text_input})
                            post_question_api(data)
                with col2:
                    st.image(image_path, width=200)
            else:
                st.warning(f"Image file not found: {image_file}")

    # Function to render welcome page
    def render_welcome_page():
        st.title("Welcome to Our App")
        st.write("Welcome to our app! We're glad to have you here.")

    # Function to handle questionnaire form
    def handle_questionnaire(question_data, image_folder):
        question = question_data.get("question", "")
        question_type = question_data.get("question_type", "")
        option_list = question_data.get("option_list", [])
        done = question_data.get("done", False)

        st.title(question)

        if question_type.lower() == "like":
            st.write("👍")
        elif question_type.lower() == "dislike":
            st.write("👎")

        render_options(question, question_type, done, option_list, image_folder)

        done = question_data.get("done", False)
        
        if done:
            col1, col2 = st.columns([3, 1])
            with col1:
                # Render "Done" button aligned to the right
                st.write("")  # Placeholder to maintain alignment
            with col2:
                # Button to call another API
                if st.button("Done", key="done_button"):
                    # Call another API here
                    render_welcome_page()

    # Define the folder path where images are located
    image_folder = "frontend\\images"

    # Render appropriate page based on input data
    data = st.session_state.get("question_data")
    if data:
        handle_questionnaire(data, image_folder)
    else:
        handle_questionnaire(post_question_api({"Like": [], "Dislike": [], "Done": False}), image_folder)

# Run the app
if __name__ == "__main__":
    main()
