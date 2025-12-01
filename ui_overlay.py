import cv2
import numpy as np
import mediapipe as mp

# ==============================
#  Utility: Draw Rounded Rectangle
# ==============================

def rounded_box(img, text, center, size, box_color, text_color, radius=20, thickness=-1, icon_path=None):
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

    if icon_path:
        icon = cv2.imread(icon_path)
        if icon is not None:
            # Pastikan frame cukup besar untuk menampung ikon
            if img.shape[0] > 30 and img.shape[1] > 30:
                icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB)
                icon = cv2.resize(icon, (30, 30))
                
                # Hitung posisi ikon
                icon_y = y - 15
                icon_x = x2 - 40

                # Pastikan ikon tidak digambar di luar batas frame
                if icon_y >= 0 and icon_y + 30 <= img.shape[0] and \
                   icon_x >= 0 and icon_x + 30 <= img.shape[1]:
                    img[icon_y:icon_y+30, icon_x:icon_x+30] = icon
        else:
            print(f"⚠️ Gagal memuat gambar ikon: {icon_path}")

    return img


# ==============================
#  Main Overlay Function
# ==============================

def draw_tiktok_style_overlay(frame, face_landmarks, question, optionA, optionB, user_answer=None, correct_answer=None):
    h, w, _ = frame.shape

    # Ambil landmark kepala (misal: dahi) pakai titik 10
    head = face_landmarks.landmark[10]
    head_x, head_y = int(head.x * w), int(head.y * h)

    # Sesuaikan posisi vertikal agar filter berada di atas kepala
    question_y = head_y - 220  # Naikkan posisi kotak pertanyaan
    option_y = head_y - 100   # Naikkan posisi pilihan jawaban

    # ======== DRAW QUESTION BOX ========
    # Create a smaller box for the "Guess The Hero" text, similar to "True/False"
    rounded_box(
        frame,
        text="Guess The Hero",
        center=(head_x, question_y - 50), # Position it above the main question
        size=(250, 40),
        box_color=(0, 0, 0), # Black background
        text_color=(255, 255, 255),
        radius=15
    )
    rounded_box(
        frame,
        text=question,
        center=(head_x, question_y),
        size=(400, 70),
        box_color=(220, 40, 40), # Reddish color
        text_color=(255, 255, 255),
        radius=25
    )

    # Determine icon for options based on user answer
    icon_a = None
    icon_b = None
    box_color_a = (40, 180, 40) # Greenish
    box_color_b = (40, 180, 40) # Greenish

    if user_answer is not None:
        if user_answer == correct_answer:
            if user_answer == "A":
                icon_a = "assets/ui/correct.jpg"
            else: # user_answer == "B"
                icon_b = "assets/ui/correct.jpg"
        else: # wrong answer
            if user_answer == "A":
                icon_a = "assets/ui/wrong.jpg"
            else: # user_answer == "B"
                icon_b = "assets/ui/wrong.jpg"


    # ======== DRAW OPTION A (LEFT) ========
    rounded_box(
        frame,
        text=optionA,
        center=(head_x - 120, option_y),
        size=(200, 80),
        box_color=box_color_a,
        text_color=(255, 255, 255),
        radius=20,
        icon_path=icon_a
    )

    # ======== DRAW OPTION B (RIGHT) ========
    rounded_box(
        frame,
        text=optionB,
        center=(head_x + 120, option_y),
        size=(200, 80),
        box_color=box_color_b,
        text_color=(255, 255, 255),
        radius=20,
        icon_path=icon_b
    )

    return frame
