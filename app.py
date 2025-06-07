import streamlit as st
import numpy as np
import cv2
from PIL import Image
import time

st.set_page_config(page_title="Live Calorie Tracker", layout="wide")

st.title("🏃‍♂️ Live Calorie Tracker using Webcam")

with st.sidebar:
    st.header("User Details")
    name = st.text_input("Enter your name", "John Doe")
    weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=200.0, value=70.0)

st.write("### Use the camera below to start your exercise session.")
frame_placeholder = st.empty()
start_button = st.button("Start Tracking")

if "prev_gray" not in st.session_state:
    st.session_state.prev_gray = None
if "total_motion" not in st.session_state:
    st.session_state.total_motion = 0
if "started" not in st.session_state:
    st.session_state.started = False

def calculate_motion(prev_gray, current_gray):
    diff = cv2.absdiff(prev_gray, current_gray)
    motion = np.sum(diff > 25)
    return motion

if start_button:
    st.session_state.started = True
    st.session_state.prev_gray = None
    st.session_state.total_motion = 0
    st.success("Started calorie tracking! Move in front of the camera.")

if st.session_state.started:
    camera_input = st.camera_input("📷 Show your exercise movement here")
    
    if camera_input is not None:
        # Read image bytes to numpy array
        img = Image.open(camera_input)
        frame = np.array(img)
        
        # Convert RGB to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Convert to gray and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if st.session_state.prev_gray is None:
            st.session_state.prev_gray = gray
            st.info("Keep moving...")
        else:
            motion = calculate_motion(st.session_state.prev_gray, gray)
            st.session_state.total_motion += motion
            st.session_state.prev_gray = gray
            
            # Show motion count live
            frame_placeholder.markdown(f"**Motion intensity:** {motion}")
            
        # Show current frame
        frame_placeholder.image(frame, channels="BGR")
    
    # Button to stop and show results
    stop_button = st.button("Stop & Show Results")
    
    if stop_button:
        # Calculate calories burned (rough estimate)
        motion_factor = st.session_state.total_motion / 1e5  # scaling factor
        calories = motion_factor * weight * 0.05
        
        st.session_state.started = False
        st.session_state.prev_gray = None
        
        st.success(f"🧍 {name}, estimated calories burned: **{calories:.2f} kcal**")
        st.info(f"Total motion detected: {st.session_state.total_motion}")
