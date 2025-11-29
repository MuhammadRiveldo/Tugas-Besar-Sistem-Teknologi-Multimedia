import cv2
import mediapipe as mp
from question_manager import get_question
from audio_manager import play_audio, stop_audio
from tilt_detector import get_head_tilt_direction
from ui_overlay import draw_tiktok_style_overlay
from video_processor import draw_result
import time

# Inisialisasi MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
score = 0
question_count = 0
should_exit = False

# === COUNTDOWN SEBELUM MULAI ===
play_audio("assets/sfx/countdown.mp3", block=False)
for i in range(5, 0, -1):
    start_time = time.time()
    while time.time() - start_time < 1:
        ret, frame = cap.read()
        if not ret:
            should_exit = True
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Tampilkan teks countdown
        text = str(i)
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 2.5, 5)
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 5)

        # Tampilkan tips cara bermain
        tip_text = "Miringkan kepala ke kiri atau kanan untuk menjawab"
        tip_text_size, _ = cv2.getTextSize(tip_text, cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)
        tip_text_x = (w - tip_text_size[0]) // 2
        tip_text_y = text_y + 70  # Di bawah angka countdown
        cv2.putText(frame, tip_text, (tip_text_x, tip_text_y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)


        cv2.imshow("Guess The Hero!", frame)
        if cv2.waitKey(1) & 0xFF == 27: # Tombol Esc
            should_exit = True
            break
    if should_exit:
        break


while not should_exit and question_count < 5:  # Game loop utama
    # === AMBIL SOAL BARU ===
    correct, options, correct_answer = get_question()

    # === SUARA HERO TIDAK LANGSUNG DIPUTAR ===
    # play_audio(correct["voice"], block=False) # Dipindahkan

    user_answer = None
    answer_time = None
    answered = False
    face_detected_first_time = False
    face_was_previously_detected = False

    # Loop untuk mendeteksi jawaban
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konversi ke RGB di awal
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Cerminkan frame agar seperti cermin
        frame_display = frame.copy()
        h, w, c = frame.shape

        # Frame sudah dalam format RGB
        results = face_mesh.process(frame)

        face_landmarks = None
        if results.multi_face_landmarks:
            if not face_detected_first_time:
                # Putar SFX dulu, lalu suara hero menggunakan callback on_finish
                # Ini tidak akan memblokir loop utama, sehingga tidak ada lag.
                play_audio(
                    "assets/sfx/show.mp3",
                    block=False,
                    on_finish=lambda: play_audio(correct["voice"], block=False)
                )
                face_detected_first_time = True
            
            # Hapus pemutaran sfx show2 agar tidak memotong suara hero
            # elif not face_was_previously_detected:
            #     play_audio("assets/sfx/show2.mp3", block=False)
            
            face_was_previously_detected = True

            face_landmarks = results.multi_face_landmarks[0]

            # Gambar UI TikTok Style
            frame_display = draw_tiktok_style_overlay(
                frame_display,
                face_landmarks=face_landmarks,
                question=f"Suara Siapakah Hero ini?",
                optionA=options['A'],
                optionB=options['B']
            )

            # Deteksi gerakan kepala jika belum ada jawaban
            if user_answer is None:
                direction = get_head_tilt_direction(face_landmarks)
                if direction == "LEFT":
                    user_answer = "A"
                    answer_time = cv2.getTickCount()
                    stop_audio()
                elif direction == "RIGHT":
                    user_answer = "B"
                    answer_time = cv2.getTickCount()
                    stop_audio()

        # Jika tidak ada wajah, tampilkan pesan
        else:
            face_was_previously_detected = False
            text = "Wajah tidak terdeteksi"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
            text_x = (w - text_size[0]) // 2
            text_y = (h + text_size[1]) // 2
            cv2.putText(frame_display, text, (text_x, text_y),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)


        # Jika sudah ada jawaban, tampilkan hasilnya
        if user_answer is not None:
            correct_bool = (user_answer == correct_answer)
            if not answered:
                if correct_bool:
                    score += 1
                    play_audio("assets/sfx/correct.mp3", block=False)
                else:
                    play_audio("assets/sfx/wrong.mp3", block=False)
                answered = True

            # Tampilkan feedback benar/salah
            frame_display = draw_result(frame_display, correct["image"], correct_bool)

            # Tampilkan hasil selama 3 detik
            if (cv2.getTickCount() - answer_time) / cv2.getTickFrequency() > 3:
                break  # Lanjut ke soal berikutnya

        # Tampilkan skor
        cv2.putText(frame_display, f"Score: {score}/5", (w - 200, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        # Konversi kembali ke BGR untuk ditampilkan oleh OpenCV
        display_bgr = cv2.cvtColor(frame_display, cv2.COLOR_RGB2BGR)
        cv2.imshow("Guess The Hero!", display_bgr)

        if cv2.waitKey(1) & 0xFF == 27: # Tombol Esc
            should_exit = True
            break

    question_count += 1
    if should_exit:
        break

# === TAMPILKAN LAYAR AKHIR ===
final_sound_played = False
while not should_exit:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Tentukan pesan berdasarkan skor
    if score <= 3:
        final_message = "Yay!!!, try again."
        sfx_path = "assets/sfx/loser.mp3"
    elif score == 4:
        final_message = "Good Job!"
        sfx_path = "assets/sfx/good job.mp3"
    else: # score == 5
        final_message = "Perfect!!!"
        sfx_path = "assets/sfx/perfect.mp3"

    if not final_sound_played:
        play_audio(sfx_path, block=False)
        final_sound_played = True

    # Tampilkan skor akhir
    score_text = f"Your Score: {score}/5"
    score_text_size, _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_DUPLEX, 2, 3)
    score_text_x = (w - score_text_size[0]) // 2
    score_text_y = (h // 2) - 50
    cv2.putText(frame, score_text, (score_text_x, score_text_y), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 3)

    # Tampilkan pesan akhir
    message_text_size, _ = cv2.getTextSize(final_message, cv2.FONT_HERSHEY_DUPLEX, 1.5, 2)
    message_text_x = (w - message_text_size[0]) // 2
    message_text_y = score_text_y + 100
    cv2.putText(frame, final_message, (message_text_x, message_text_y), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 0), 2)

    # Tampilkan instruksi keluar
    exit_text = "Press 'Esc' to exit"
    exit_text_size, _ = cv2.getTextSize(exit_text, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
    exit_text_x = (w - exit_text_size[0]) // 2
    exit_text_y = h - 50
    cv2.putText(frame, exit_text, (exit_text_x, exit_text_y), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    cv2.imshow("Guess The Hero!", frame)

    if cv2.waitKey(1) & 0xFF == 27: # Tombol Esc
        break


face_mesh.close()
cap.release()
cv2.destroyAllWindows()
