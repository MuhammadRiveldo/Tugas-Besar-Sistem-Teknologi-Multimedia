import cv2
import numpy as np
from question_manager import get_question
from audio_manager import play_audio
from head_movement import detect_head_direction
from video_processor import draw_options, draw_result, detect_face
from utils import countdown

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("results/output.mp4", fourcc, 20, (640,480))

while True: # Game loop utama
    # === AMBIL SOAL BARU ===
    correct, options, correct_answer = get_question()

    print("Soal:", correct["name"])
    print("Options:", options)

    # === PLAY SUARA HERO ===
    play_audio(correct["voice"])

    print("Silakan tebak dengan gerak kepala...")

    user_answer = None
    answer_time = None

    # Loop untuk mendeteksi jawaban
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1) # Cerminkan frame agar seperti cermin
        
        # Deteksi wajah
        frame, face_coords = detect_face(frame)
        
        frame_display = frame.copy()

        # Gambar opsi
        frame_display = draw_options(frame_display, options)

        # Deteksi gerakan kepala jika belum ada jawaban
        if user_answer is None:
            direction = detect_head_direction(frame, face_coords)
            if direction == "LEFT":
                user_answer = "A"
                answer_time = cv2.getTickCount()
                # Putar suara hanya sekali saat jawaban benar pertama kali
                if user_answer == correct_answer:
                    play_audio(correct["voice"])
            elif direction == "RIGHT":
                user_answer = "B"
                answer_time = cv2.getTickCount()
                # Putar suara hanya sekali saat jawaban benar pertama kali
                if user_answer == correct_answer:
                    play_audio(correct["voice"])

        # Jika sudah ada jawaban, tampilkan hasilnya
        if user_answer is not None:
            correct_bool = (user_answer == correct_answer)
            frame_display = draw_result(frame_display, correct["image"], correct_bool)

            # Tampilkan hasil selama 3 detik
            if (cv2.getTickCount() - answer_time) / cv2.getTickFrequency() > 3:
                break # Lanjut ke soal berikutnya

        writer.write(frame_display)
        cv2.imshow("Guess The Hero!", frame_display)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
