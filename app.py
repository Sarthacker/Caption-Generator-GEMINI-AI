import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.title('Photo Descriptor')

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "png", "jpeg"])

API_KEY = st.text_input("Enter your API Key: ", type="password")
if uploaded_file is not None:
    if st.button('Generate The Caption'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            file_path = os.path.join(uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            img = Image.open(file_path)
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-pro-vision')
                caption = model.generate_content(["Write a caption for the image in english",img])
                tags=model.generate_content(["Generate 5 hash tags for the image in a line in english",img])
                st.image(img, caption=f"Caption: {caption.text}")
                st.write(f"Tags: {tags.text}")
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"Failed to configure API due to {error_msg}")