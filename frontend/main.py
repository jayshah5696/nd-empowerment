import streamlit as st
import requests

# Function to make POST request to Flask API
def post_question_api(data):
    url = "http://localhost:5000/api/question"  # Change URL accordingly
    response = requests.post(url, json=data)
    return response.json()

# Main Streamlit app
def main():
    st.title("Questionnaire App")

    # Function to render options
    def render_options(option_list):
        for option in option_list:
            st.subheader(option.get("Text_input", ""))
            st.image(option.get("Image", ""), width=200)

    # Function to render welcome page
    def render_welcome_page():
        st.title("Welcome to Our App")
        st.write("Welcome to our app! We're glad to have you here.")

    # Function to handle questionnaire form
    def handle_questionnaire(question_data):
        question = question_data.get("question", "")
        question_type = question_data.get("question_type", "")
        option_list = question_data.get("option_list", [])

        st.title("Question:")
        st.write(question)

        if question_type.lower() == "like":
            st.write("👍")
        elif question_type.lower() == "dislike":
            st.write("👎")

        render_options(option_list)

        done = question_data.get("done", False)
        if done:
            st.write("Thank you for completing the questionnaire!")

    # Render appropriate page based on input data
    data = st.session_state.get("question_data")
    if data:
        handle_questionnaire(data)
        if data.get("done", False):
            render_welcome_page()
    else:
        st.write("Please wait for the questionnaire data to load...")

# Run the app
if __name__ == "__main__":
    main()
