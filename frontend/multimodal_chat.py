import streamlit as st
import base64
from pathlib import Path
import csv
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img

# Mock functions for speech-to-text and text-to-speech conversion
def speech_to_text(audio_data):
    # Mock function for speech-to-text conversion
    return "This is a mock response for the audio input."

def text_to_speech(text):
    # Mock function for text-to-speech conversion
    # Assume here you have a function that converts text to audio
    # and returns the path to the generated audio file
    # For demonstration, let's just return a sa
    return "path/to/generated/audio/file.mp3"

def csv_to_dict(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        result = {row['Text Input']: row['Location'] for row in reader}
    return result



def multimodal_chat():
    dict_items = csv_to_dict("journal_entries.csv")
    # filter the dict items if values are not empty
    dict_items = {k: v for k, v in dict_items.items() if v}

    options = dict_items.keys()
    selected_option = st.selectbox("Select a journal entry", options)
    with open(dict_items[selected_option], "r") as file:
        markdown_content = file.read()
        response = markdown_content
    st.markdown(markdown_content, unsafe_allow_html=True)
    

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "assistant" and message.get("content_type") == "audio":
            st.audio(message["content"], format="audio/mp3")  # Display audio output
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt, unsafe_allow_html=True)

        with st.chat_message("assistant"):

            # Mock text plus image response

            # Path to your local image file
            # local_img_path = "C:\\Apps\\nd-empowerment\\frontend\\images\\sample2.jpg"
            # local_img_path = "images/sample1.jpg"

            # # Convert the local image to base64
            # encoded_img = img_to_bytes(local_img_path)

            # # Create the HTML string with the base64-encoded image
            # html = f'<p>Hi mr lion king</p><img src="data:image/png;base64,{encoded_img}" alt="Local Image">'
            response = "Hi"

            st.session_state.messages.append({"role": "assistant", "content": response})
