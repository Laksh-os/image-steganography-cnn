import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from stego import hide_text

st.title("🔐 Image Steganography using CNN")

# Load model
model = load_model("stego_cnn_model.h5")

uploaded = st.file_uploader("Upload Image", type=["png", "jpg"])
secret = st.text_input("Enter Secret Message")

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Original Image")

    if st.button("Hide Message"):
        stego_img = hide_text(image, secret)
        st.image(stego_img, caption="Stego Image")

        # Prepare image for CNN
        img = stego_img.resize((128, 128))
        img = np.array(img) / 255.0
        img = img.reshape(1, 128, 128, 3)

        pred = model.predict(img)

        if pred[0][0] > 0.5:
            st.success("🔍 CNN Detection: Stego Image")
        else:
            st.info("🔍 CNN Detection: Cover Image")

