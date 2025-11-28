import cv2
import numpy as np
import mediapipe as mp

# ==============================
#  Utility: Draw Rounded Rectangle
# ==============================

def rounded_box(img, text, center, size, box_color, text_color, radius=20, thickness=-1):
    w, h = size
    x, y = center

    x1, y1 = int(x - w//2), int(y - h//2)
    x2, y2 = int(x + w//2), int(y + h//2)

    # Rounded rectangle
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), box_color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), box_color, thickness)

    # Corner circles
    cv2.circle(img, (x1 + radius, y1 + radius), radius, box_color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, box_color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, box_color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, box_color, thickness)

    # Add text
    cv2.putText(img, text, (x1 + 20, y + 10),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, text_color, 2)

    return img


# ==============================
#  Main Overlay Function
# ==============================

def draw_tiktok_style_overlay(frame, face_landmarks, question, optionA, optionB):
    h, w, _ = frame.shape

    # Ambil landmark kepala (misal: dahi) pakai titik 10
    head = face_landmarks.landmark[10]
    head_x, head_y = int(head.x * w), int(head.y * h)

    # Sesuaikan posisi vertikal agar filter berada di atas kepala
    question_y = head_y - 220  # Naikkan posisi kotak pertanyaan
    option_y = head_y - 100   # Naikkan posisi pilihan jawaban

    # ======== DRAW QUESTION BOX ========
    rounded_box(
        frame,
        text=question,
        center=(head_x, question_y),
        size=(400, 70),
        box_color=(255, 0, 0),
        text_color=(255, 255, 255),
        radius=25
    )

    # ======== DRAW OPTION A (LEFT) ========
    rounded_box(
        frame,
        text=optionA,
        center=(head_x - 120, option_y),
        size=(200, 80),
        box_color=(0, 255, 0),
        text_color=(255, 255, 255),
        radius=20
    )

    # ======== DRAW OPTION B (RIGHT) ========
    rounded_box(
        frame,
        text=optionB,
        center=(head_x + 120, option_y),
        size=(200, 80),
        box_color=(0, 255, 0),
        text_color=(255, 255, 255),
        radius=20
    )

    return frame
