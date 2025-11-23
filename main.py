import cv2
import numpy as np
from question_manager import get_question
from audio_manager import play_audio, stop_audio
from head_movement import detect_head_direction
from video_processor import draw_options, draw_result, detect_face
from utils import countdown

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("results/output.mp4", fourcc, 20, (640,480))

score = 0

while score < 5: # Game loop utama
    # === AMBIL SOAL BARU ===
    correct, options, correct_answer = get_question()

    print("Soal:", correct["name"])
    print("Options:", options)

    # Loop untuk menampilkan kamera sebelum suara diputar
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_display = frame.copy()
        frame_display = draw_options(frame_display, options, score)
        cv2.imshow("Guess The Hero!", frame_display)

        # Tampilkan frame selama 1ms dan cek apakah user ingin keluar
        if cv2.waitKey(1) & 0xFF == 27:
            cap.release()
            writer.release()
            cv2.destroyAllWindows()
            exit()
        
        # Beri jeda singkat agar window sempat muncul
        if cv2.waitKey(100) & 0xFF != 27:
             break

    # === PLAY SUARA HERO (Non-Blocking) ===
    play_audio(correct["voice"], block=False)

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
        frame_display = draw_options(frame_display, options, score)

        # Deteksi gerakan kepala jika belum ada jawaban
        if user_answer is None:
            direction = detect_head_direction(frame, face_coords)
            if direction == "LEFT":
                user_answer = "A"
                answer_time = cv2.getTickCount()
                stop_audio()
            elif direction == "RIGHT":
                user_answer = "B"
                answer_time = cv2.getTickCount()
                stop_audio()

        # Jika sudah ada jawaban, tampilkan hasilnya
        if user_answer is not None:
            correct_bool = (user_answer == correct_answer)
            if 'answered' not in locals():
                if correct_bool:
                    score += 1
                answered = True

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

    del locals()['answered']

cap.release()
writer.release()
cv2.destroyAllWindows()
