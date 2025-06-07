import streamlit as st
import cv2
from helper import estimate_calories
import time

# Page config
st.set_page_config(page_title="🏃‍♂️ Exercise Calorie Tracker", layout="wide")
st.title("🏋️ Real-Time Exercise Calorie Counter")

# Sidebar inputs
st.sidebar.header("📝 User Details")
name = st.sidebar.text_input("Enter your name")
weight = st.sidebar.number_input("Enter your weight (kg)", min_value=20, max_value=200, value=70)

start_button = st.sidebar.button("Start Camera")

# Session state for calories
if 'calories' not in st.session_state:
    st.session_state.calories = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if start_button:
    st.session_state.start_time = time.time()
    st.sidebar.success("Camera started. Do some jumping/crouching!")

    # Webcam
    cap = cv2.VideoCapture(0)
    frame_window = st.empty()
    prev_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize
        frame = cv2.resize(frame, (640, 480))

        # Estimate calories
        frame, movement = estimate_calories(frame, prev_frame)
        st.session_state.calories += (movement * 0.001 * weight)

        # Display
        frame_window.image(frame, channels="BGR")

        prev_frame = frame

        # Stop with Streamlit's rerun
        if st.sidebar.button("⏹️ Stop"):
            break

    cap.release()

# Final result
if st.session_state.start_time:
    duration = round(time.time() - st.session_state.start_time, 2)
    st.success(f"✅ {name}, you burned approx. **{st.session_state.calories:.2f} calories** in **{duration} seconds**!")
