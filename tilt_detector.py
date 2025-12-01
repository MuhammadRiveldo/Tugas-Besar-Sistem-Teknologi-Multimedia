import math

def get_head_tilt_direction(face_landmarks):
    """Mendeteksi kemiringan kepala (kiri, kanan, atau tengah) dari landmark wajah."""
    if not face_landmarks:
        return "CENTER"

    # Titik referensi pada mata kiri dan kanan
    p1 = face_landmarks.landmark[33]  # Mata kiri
    p2 = face_landmarks.landmark[263] # Mata kanan

    # Hitung sudut garis yang menghubungkan kedua mata
    angle = math.degrees(math.atan2(p2.y - p1.y, p2.x - p1.x))

    # Threshold untuk menentukan kemiringan
    tilt_threshold = 15

    if angle > tilt_threshold:
        return "RIGHT"  # Sudut positif: miring ke kanan
    elif angle < -tilt_threshold:
        return "LEFT"   # Sudut negatif: miring ke kiri
    else:
        return "CENTER"
