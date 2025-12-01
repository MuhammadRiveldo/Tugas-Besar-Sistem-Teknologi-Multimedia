import cv2
import numpy as np
import mediapipe as mp

# ==============================
#  Fungsi: Gambar Kotak Bulat
# ==============================

def rounded_box(img, text, center, size, box_color, text_color, radius=20, thickness=-1, icon_path=None):
    """Menggambar kotak dengan sudut bulat, teks, dan ikon opsional."""
    w, h = size
    x, y = center

    x1, y1 = int(x - w//2), int(y - h//2)
    x2, y2 = int(x + w//2), int(y + h//2)

    # Gambar 4 persegi panjang untuk membentuk dasar kotak bulat
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), box_color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), box_color, thickness)

    # Gambar 4 lingkaran di sudut-sudut
    cv2.circle(img, (x1 + radius, y1 + radius), radius, box_color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, box_color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, box_color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, box_color, thickness)

    # Tambahkan teks di dalam kotak
    cv2.putText(img, text, (x1 + 20, y + 10),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, text_color, 2)

    if icon_path:
        # Muat ikon dengan transparansi (alpha channel)
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
        if icon is not None:
            # Pastikan frame cukup besar
            if img.shape[0] > 30 and img.shape[1] > 30:
                icon = cv2.resize(icon, (30, 30))
                
                # Hitung posisi ikon di pojok kanan bawah kotak
                padding = 5
                icon_y = y2 - 30 - padding
                icon_x = x2 - 30 - padding

                # Pastikan posisi ikon valid
                if icon_y >= 0 and icon_y + 30 <= img.shape[0] and \
                   icon_x >= 0 and icon_x + 30 <= img.shape[1]:
                    
                    # Ambil Region of Interest (ROI) dari frame
                    roi = img[icon_y:icon_y+30, icon_x:icon_x+30]

                    # Proses blending jika ikon punya alpha channel
                    if icon.shape[2] == 4:
                        # Pisahkan channel warna dan alpha
                        icon_rgb = icon[:,:,:3]
                        alpha = icon[:,:,3]

                        # Konversi ikon ke format warna frame (RGB)
                        icon_rgb = cv2.cvtColor(icon_rgb, cv2.COLOR_BGR2RGB)

                        # Buat mask untuk blending
                        mask = cv2.merge([alpha, alpha, alpha])
                        mask_inv = cv2.bitwise_not(mask)

                        # Gabungkan ikon dengan background
                        bg = cv2.bitwise_and(roi, mask_inv)
                        fg = cv2.bitwise_and(icon_rgb, mask)
                        combined = cv2.add(bg, fg)
                        
                        img[icon_y:icon_y+30, icon_x:icon_x+30] = combined
                    else:
                        # Jika tidak ada alpha, langsung timpa (fallback)
                        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB)
                        img[icon_y:icon_y+30, icon_x:icon_x+30] = icon
        else:
            print(f"⚠️ Gagal memuat gambar ikon: {icon_path}")

    return img


# ==============================
#  Fungsi: Gambar Overlay Utama
# ==============================

def draw_tiktok_style_overlay(frame, face_landmarks, question, optionA, optionB, user_answer=None, correct_answer=None):
    """Menggambar seluruh UI (pertanyaan & pilihan) yang mengikuti wajah."""
    h, w, _ = frame.shape

    # Ambil posisi dahi sebagai referensi posisi UI
    head = face_landmarks.landmark[10]
    head_x, head_y = int(head.x * w), int(head.y * h)

    # Atur posisi vertikal UI di atas kepala
    question_y = head_y - 220
    option_y = head_y - 100

    # === Gambar Kotak Pertanyaan ===
    # Judul "Guess The Hero"
    rounded_box(
        frame,
        text="Guess The Hero",
        center=(head_x, question_y - 50), # Posisikan di atas pertanyaan utama
        size=(250, 40),
        box_color=(0, 255, 0), 
        text_color=(255, 255, 255),
        radius=15
    )
    # Teks pertanyaan
    rounded_box(
        frame,
        text=question,
        center=(head_x, question_y),
        size=(400, 55),
        box_color=(191, 0, 255),
        text_color=(255, 255, 255),
        radius=25
    )

    # Tentukan ikon (benar/salah) berdasarkan jawaban user
    icon_a = None
    icon_b = None
    box_color_a = (0, 0, 255)
    box_color_b = (255, 0, 0)

    if user_answer is not None:
        is_correct = (user_answer == correct_answer)
        if is_correct:
            icon_path = "assets/ui/correct.png"
        else:
            icon_path = "assets/ui/wrong.png"
        
        if user_answer == "A":
            icon_a = icon_path
        else: # user_answer == "B"
            icon_b = icon_path


    # === Gambar Pilihan A (Kiri) ===
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

    # === Gambar Pilihan B (Kanan) ===
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
