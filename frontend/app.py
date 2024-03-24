import streamlit as st
import random
import json
from psychometry import psychometry_page
from simple_chat import simple_chat
from multimodal_chat import multimodal_chat
from journal import journal_app

with open("C:\\Apps\\nd-empowerment\\utils\\style_guide.json", "r") as file:
    json_data = json.load(file)

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ['Psychometry', 'Chat', "Multimodal Chat", "Journal"])

    if page == 'Psychometry':
        psychometry_page()
    elif page == 'Chat':
        simple_chat(json_data)
    elif page == "Multimodal Chat":
        multimodal_chat()
    elif page == "Journal":
        journal_app()



if __name__ == "__main__":
    main()
