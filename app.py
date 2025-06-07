import streamlit as st
import cv2
import tempfile
import time
import numpy as np
from utils.calorie_counter import process_video

st.set_page_config(page_title="🏃 Calorie Tracker", layout="wide")

st.title("🏃‍♂️ Real-Time Calorie Burn Estimator")
st.markdown("Upload your **exercise video** and get a calorie burn estimate based on motion intensity.")

# Input user details
with st.sidebar:
    st.header("👤 User Details")
    name = st.text_input("Enter your name", "John Doe")
    weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=200.0, value=70.0)
    uploaded_video = st.file_uploader("📹 Upload Exercise Video", type=["mp4", "mov", "avi"])

if uploaded_video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    cap = cv2.VideoCapture(tfile.name)

    st.video(tfile.name)
    st.markdown("---")
    st.subheader("📊 Calorie Burn Report")

    with st.spinner("Analyzing video and estimating calories..."):
        calories, total_motion = process_video(cap, weight)
        st.success(f"✅ Name: {name}")
        st.info(f"📏 Total Motion Detected: {total_motion:.2f}")
        st.success(f"🔥 Estimated Calories Burned: {calories:.2f} kcal")

    st.markdown("✅ This estimate is based on motion intensity and body weight. For medical accuracy, use wearables or consult professionals.")
