import streamlit as st
import base64
from pathlib import Path

# Function to convert image file to base64
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img

# Path to your local image file
local_img_path = "C:\\Apps\\nd-empowerment\\frontend\\images\\sample2.jpg"

# Convert the local image to base64
encoded_img = img_to_bytes(local_img_path)

# Create the HTML string with the base64-encoded image
html = f'<p>Hi mr lion king</p><img src="data:image/png;base64,{encoded_img}" alt="Local Image">'

# Render the HTML in Streamlit
st.markdown(html, unsafe_allow_html=True)
