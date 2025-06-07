import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np

st.title("Live Exercise Calorie Tracker with streamlit-webrtc")

name = st.text_input("Enter your name")
weight = st.number_input("Enter your weight (kg)", min_value=1.0, max_value=300.0, step=0.5)

if not name or weight == 0:
    st.warning("Please enter your name and weight")
    st.stop()

# Global state to accumulate motion and calories
if "prev_frame" not in st.session_state:
    st.session_state.prev_frame = None
if "total_motion" not in st.session_state:
    st.session_state.total_motion = 0.0

def process_frame(frame):
    img = frame.to_ndarray(format="bgr24")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if st.session_state.prev_frame is None:
        st.session_state.prev_frame = gray
        return img

    diff = cv2.absdiff(st.session_state.prev_frame, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    motion = np.sum(thresh) / 255

    st.session_state.total_motion += motion
    st.session_state.prev_frame = gray

    # Draw the motion mask on the frame
    mask_colored = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    combined = cv2.addWeighted(img, 0.7, mask_colored, 0.3, 0)

    return combined

webrtc_ctx = webrtc_streamer(
    key="exercise-calorie-tracker",
    video_frame_callback=process_frame,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

if webrtc_ctx.state.playing:
    st.write(f"Total motion so far: {st.session_state.total_motion:.2f}")

    # Simple calorie calculation
    calories = st.session_state.total_motion * weight * 0.00001
    st.write(f"Estimated calories burned: {calories:.2f} kcal")

    if st.button("Reset Tracker"):
        st.session_state.prev_frame = None
        st.session_state.total_motion = 0.0
        st.experimental_rerun()
else:
    st.info("Start the webcam stream and move to track calories.")

