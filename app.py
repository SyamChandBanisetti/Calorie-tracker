import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

st.title("🎯 Live Exercise Calorie Tracker (via Camera Capture)")

# User inputs
name = st.text_input("Enter your name:")
weight = st.number_input("Enter your weight (kg):", min_value=1.0, max_value=300.0, step=0.5)

if 'prev_gray' not in st.session_state:
    st.session_state.prev_gray = None
if 'total_motion' not in st.session_state:
    st.session_state.total_motion = 0.0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'frames_processed' not in st.session_state:
    st.session_state.frames_processed = 0

def calculate_motion(prev_gray, curr_gray, threshold=25):
    diff = cv2.absdiff(prev_gray, curr_gray)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    motion_score = np.sum(thresh) / 255
    return motion_score

st.markdown("### Step 1: Capture frames by clicking the camera below repeatedly during your exercise.")

img_file_buffer = st.camera_input("Capture a frame")

if img_file_buffer is not None and name and weight:
    # Read image bytes to numpy array
    img = Image.open(img_file_buffer)
    frame = np.array(img.convert('RGB'))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Preprocess frame for motion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if st.session_state.prev_gray is None:
        st.session_state.prev_gray = gray
        st.success("First frame captured, keep capturing to track movement...")
    else:
        motion = calculate_motion(st.session_state.prev_gray, gray)
        st.session_state.total_motion += motion
        st.session_state.frames_processed += 1
        st.session_state.prev_gray = gray

        st.write(f"Motion detected in this frame: {motion:.2f}")

    elapsed = time.time() - st.session_state.start_time
    st.write(f"Total frames processed: {st.session_state.frames_processed}")
    st.write(f"Elapsed time: {elapsed:.1f} seconds")

    # Simple calorie estimate formula (you can tweak coefficients)
    calories_burned = (st.session_state.total_motion / (elapsed + 1)) * weight * 0.0005
    st.markdown(f"### Estimated calories burned so far: **{calories_burned:.2f} kcal**")

else:
    if not name or not weight:
        st.info("Please enter your name and weight to start tracking.")
    else:
        st.info("Please capture a frame to begin.")

st.markdown("---")
st.markdown("### When done with your exercise, you can reset the tracker below.")

if st.button("Reset Tracker"):
    st.session_state.prev_gray = None
    st.session_state.total_motion = 0.0
    st.session_state.frames_processed = 0
    st.session_state.start_time = time.time()
    st.success("Tracker reset! Start capturing frames again.")

