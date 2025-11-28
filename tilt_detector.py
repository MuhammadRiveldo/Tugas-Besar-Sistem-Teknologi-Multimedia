import math

def get_head_tilt_direction(face_landmarks):
    if not face_landmarks:
        return "CENTER"

    # Get the coordinates of the left and right eye landmarks
    p1 = face_landmarks.landmark[33]  # Left eye
    p2 = face_landmarks.landmark[263] # Right eye

    # Calculate the angle of the line connecting the two eye landmarks
    angle = math.degrees(math.atan2(p2.y - p1.y, p2.x - p1.x))

    # Define the thresholds for head tilt
    tilt_threshold = 15

    if angle > tilt_threshold:
        return "LEFT"
    elif angle < -tilt_threshold:
        return "RIGHT"
    else:
        return "CENTER"
