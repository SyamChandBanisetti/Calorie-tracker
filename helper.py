import cv2
import numpy as np

def estimate_calories(frame, prev_frame):
    movement = 0

    if prev_frame is not None:
        # Convert to grayscale
        gray1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute frame difference
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Calculate motion magnitude
        movement = np.sum(thresh) / 255  # white pixel count = motion

        # Show movement score
        cv2.putText(frame, f"Motion: {int(movement)}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    return frame, movement
