import cv2
import mediapipe as mp
from question_manager import get_question
from audio_manager import play_audio, stop_audio
from tilt_detector import get_head_tilt_direction
from ui_overlay import draw_tiktok_style_overlay
from video_processor import draw_result
import time

# Inisialisasi MediaPipe & OpenCV
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
window_name = "Guess The Hero!"
cv2.namedWindow(window_name)

# === Loop Utama Game (untuk replay) ===
while True:
    score = 0
    question_count = 0
    should_exit = False

    # === Countdown Sebelum Mulai ===
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

            # Tampilkan tips bermain
            tip_text = "Miringkan kepala ke kiri atau kanan untuk menjawab"
            tip_text_size, _ = cv2.getTextSize(tip_text, cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)
            tip_text_x = (w - tip_text_size[0]) // 2
            tip_text_y = text_y + 70  # Di bawah angka countdown
            cv2.putText(frame, tip_text, (tip_text_x, tip_text_y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Tombol Esc
                should_exit = True
                break
        if should_exit:
            break

    # === Mulai Timer Game ===
    game_start_time = time.time()

    while not should_exit and question_count < 5:  # Loop per pertanyaan
        # === Ambil Soal Baru ===
        correct, options, correct_answer = get_question()

        # Variabel untuk status jawaban per soal
        user_answer = None
        answer_time = None
        answered = False
        face_detected_first_time = False
        face_was_previously_detected = False

        # Loop untuk satu pertanyaan (deteksi wajah & jawaban)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Konversi BGR ke RGB dan flip frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            frame_display = frame.copy()
            h, w, c = frame.shape

            # Proses frame dengan Face Mesh
            results = face_mesh.process(frame)

            face_landmarks = None
            if results.multi_face_landmarks:
                if not face_detected_first_time:
                    # Putar SFX dan suara hero saat wajah pertama kali terdeteksi
                    play_audio(
                        "assets/sfx/show.mp3",
                        block=False,
                        on_finish=lambda: play_audio(correct["voice"], block=False)
                    )
                    face_detected_first_time = True
                
                face_was_previously_detected = True

                face_landmarks = results.multi_face_landmarks[0]

                # Gambar overlay UI (pertanyaan & pilihan)
                frame_display = draw_tiktok_style_overlay(
                    frame_display,
                    face_landmarks=face_landmarks,
                    question=f"Suara Siapakah Hero ini?",
                    optionA=options['A'],
                    optionB=options['B'],
                    user_answer=user_answer,
                    correct_answer=correct_answer
                )

                # Deteksi jawaban dari kemiringan kepala
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

            # Jika wajah tidak terdeteksi
            else:
                face_was_previously_detected = False
                text = "Wajah tidak terdeteksi"
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
                text_x = (w - text_size[0]) // 2
                text_y = (h + text_size[1]) // 2
                cv2.putText(frame_display, text, (text_x, text_y),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

            # Jika sudah menjawab, proses hasilnya
            if user_answer is not None:
                correct_bool = (user_answer == correct_answer)
                if not answered:
                    if correct_bool:
                        score += 1
                        play_audio("assets/sfx/correct.mp3", block=False)
                    else:
                        play_audio("assets/sfx/wrong.mp3", block=False)
                    answered = True

                # Tampilkan gambar hero sebagai feedback
                frame_display = draw_result(frame_display, correct["image"])

                # Tunggu 3 detik sebelum ke soal berikutnya
                if (cv2.getTickCount() - answer_time) / cv2.getTickFrequency() > 3:
                    break  # Lanjut ke soal berikutnya

            # Tampilkan skor
            cv2.putText(frame_display, f"Score: {score}/5", (w - 200, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

            # Konversi kembali ke BGR untuk display
            display_bgr = cv2.cvtColor(frame_display, cv2.COLOR_RGB2BGR)
            cv2.imshow(window_name, display_bgr)

            if cv2.waitKey(1) & 0xFF == 27:  # Tombol Esc
                should_exit = True
                break

        question_count += 1
        if should_exit:
            break

    # === Selesai Game ===
    game_end_time = time.time()
    total_game_time = game_end_time - game_start_time

    # === Tampilkan Layar Akhir (Skor & Opsi Main Lagi) ===
    final_sound_played = False
    play_again_pressed = False
    while not should_exit and not play_again_pressed:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Tentukan pesan & SFX berdasarkan skor
        if score <= 3:
            final_message = "Yay!!!, try again."
            sfx_path = "assets/sfx/loser.mp3"
        elif score == 4:
            final_message = "Good Job!"
            sfx_path = "assets/sfx/good job.mp3"
        else:  # score == 5
            final_message = "Perfect!!!"
            sfx_path = "assets/sfx/perfect.mp3"

        if not final_sound_played:
            play_audio(sfx_path, block=False)
            final_sound_played = True

        # Tampilkan skor akhir
        score_text = f"Your Score: {score}/5"
        score_text_size, _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_DUPLEX, 2, 3)
        score_text_x = (w - score_text_size[0]) // 2
        score_text_y = (h // 2) - 100
        cv2.putText(frame, score_text, (score_text_x, score_text_y), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 3)

        # Tampilkan total waktu bermain
        time_text = f"Time: {total_game_time:.2f} seconds"
        time_text_size, _ = cv2.getTextSize(time_text, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
        time_text_x = (w - time_text_size[0]) // 2
        time_text_y = score_text_y + 80
        cv2.putText(frame, time_text, (time_text_x, time_text_y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        # Tampilkan pesan final
        message_text_size, _ = cv2.getTextSize(final_message, cv2.FONT_HERSHEY_DUPLEX, 1.5, 2)
        message_text_x = (w - message_text_size[0]) // 2
        message_text_y = time_text_y + 100
        cv2.putText(frame, final_message, (message_text_x, message_text_y), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 0), 2)

        # Tombol visual "Play Again"
        button_w, button_h = 450, 60
        button_x = (w - button_w) // 2
        button_y = message_text_y + 100
        cv2.rectangle(frame, (button_x, button_y), (button_x + button_w, button_y + button_h), (0, 200, 0), -1)
        button_text = "Press SPACE to Play Again"
        button_text_size, _ = cv2.getTextSize(button_text, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
        button_text_x = button_x + (button_w - button_text_size[0]) // 2
        button_text_y = button_y + (button_h + button_text_size[1]) // 2
        cv2.putText(frame, button_text, (button_text_x, button_text_y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        # Tampilkan instruksi keluar
        exit_text = "Press 'Esc' to exit"
        exit_text_size, _ = cv2.getTextSize(exit_text, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
        exit_text_x = (w - exit_text_size[0]) // 2
        exit_text_y = h - 50
        cv2.putText(frame, exit_text, (exit_text_x, exit_text_y), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Tombol Esc
            should_exit = True
            break
        elif key == 32:  # Tombol Spasi
            play_again_pressed = True
            break
    
    if should_exit:
        break  # Keluar dari loop utama game

face_mesh.close()
cap.release()
cv2.destroyAllWindows()
