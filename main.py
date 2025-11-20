import cv2
import numpy as np
from question_manager import get_question
from audio_manager import play_audio
from head_movement import detect_head_direction
from video_processor import draw_options, draw_result
from utils import countdown

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("results/output.mp4", fourcc, 20, (640,480))

# === AMBIL SOAL BARU ===
correct, options, correct_answer = get_question()

print("Soal:", correct)
print("Options:", options)

# === PLAY SUARA HERO ===
play_audio(correct["voice"])

print("Silakan tebak dengan gerak kepala...")

user_answer = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Gambar opsi
    frame = draw_options(frame, options)

    direction = detect_head_direction(frame)

    if direction == "LEFT":
        user_answer = "A"
        break
    elif direction == "RIGHT":
        user_answer = "B"
        break

    writer.write(frame)
    cv2.imshow("Guess The Hero!", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# === CEK BENAR/SALAH ===
correct_bool = (user_answer == correct_answer)

result_frame = draw_result(frame, correct["image"], correct_bool)
writer.write(result_frame)

# === TAMPIL 3 DETIK ===
cv2.imshow("Guess The Hero!", result_frame)
cv2.waitKey(3000)

cap.release()
writer.release()
cv2.destroyAllWindows()
