import cv2
import numpy as np

def process_video(cap, weight):
    total_motion = 0
    calories = 0
    prev_gray = None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_time = 1.0 / fps if fps > 0 else 1.0 / 30

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_gray is None:
            prev_gray = gray
            continue

        diff = cv2.absdiff(prev_gray, gray)
        motion = np.sum(diff > 25)
        total_motion += motion

        prev_gray = gray

    # Normalize and calculate calories based on rough empirical values
    motion_factor = total_motion / 1e6  # scale down large numbers
    calories = motion_factor * weight * 0.05  # estimated factor

    cap.release()
    return calories, total_motion
