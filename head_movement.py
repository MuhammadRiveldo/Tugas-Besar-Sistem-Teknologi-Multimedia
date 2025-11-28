def detect_head_direction(frame, face_coords):
    if face_coords is None:
        return "NONE", 0

    (x, y, w, h) = face_coords
    face_center_x = x + w / 2
    frame_center_x = frame.shape[1] / 2
    
    # Calculate the horizontal distance from the center
    distance = face_center_x - frame_center_x

    # Tentukan ambang batas pergerakan
    threshold = 50  # bisa disesuaikan

    if face_center_x < frame_center_x - threshold:
        return "LEFT"
    elif face_center_x > frame_center_x + threshold:
        return "RIGHT"
    else:
        return "CENTER"
