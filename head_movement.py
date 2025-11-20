import mediapipe as mp

mp_face = mp.solutions.face_mesh.FaceMesh(static_image_mode=False)

def detect_head_direction(frame):
    results = mp_face.process(frame)

    if not results.multi_face_landmarks:
        return "NONE"

    # Ambil landmark hidung
    lm = results.multi_face_landmarks[0].landmark
    nose_x = lm[1].x  # titik hidung

    # threshold kiri-kanan
    if nose_x < 0.43:
        return "LEFT"
    elif nose_x > 0.57:
        return "RIGHT"
    else:
        return "CENTER"
