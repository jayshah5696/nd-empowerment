import streamlit as st
import random
from psychometry import psychometry_page
from simple_chat import simple_chat
from multimodal_chat import multimodal_chat

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ['Psychometry', 'Chat', "Multimodal Chat"])

    if page == 'Psychometry':
        psychometry_page()
    elif page == 'Chat':
        simple_chat(f"Mocked response from assistant. {random.randint(1, 100)}")
    elif page == "Multimodal Chat":
        multimodal_chat()



if __name__ == "__main__":
    main()
