import cv2
import mediapipe as mp
from question_manager import get_question
from audio_manager import play_audio, stop_audio
from tilt_detector import get_head_tilt_direction
from ui_overlay import draw_tiktok_style_overlay
from video_processor import draw_result

# Inisialisasi MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
score = 0

while score < 5:  # Game loop utama
    # === AMBIL SOAL BARU ===
    correct, options, correct_answer = get_question()

    print("Soal:", correct["name"])
    print("Options:", options)

    # === PLAY SUARA HERO (Non-Blocking) ===
    play_audio(correct["voice"], block=False)
    print("Silakan tebak dengan memiringkan kepala...")

    user_answer = None
    answer_time = None
    answered = False

    # Loop untuk mendeteksi jawaban
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Cerminkan frame agar seperti cermin
        frame_display = frame.copy()
        h, w, c = frame.shape

        # Konversi warna BGR ke RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        face_landmarks = None
        if results.multi_face_landmarks:
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
            cv2.putText(frame_display, "Wajah tidak terdeteksi", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        # Jika sudah ada jawaban, tampilkan hasilnya
        if user_answer is not None:
            correct_bool = (user_answer == correct_answer)
            if not answered:
                if correct_bool:
                    score += 1
                answered = True

            # Tampilkan feedback benar/salah
            frame_display = draw_result(frame_display, correct["image"], correct_bool)

            # Tampilkan hasil selama 3 detik
            if (cv2.getTickCount() - answer_time) / cv2.getTickFrequency() > 3:
                break  # Lanjut ke soal berikutnya

        # Tampilkan skor
        cv2.putText(frame_display, f"Score: {score}/5", (w - 200, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Guess The Hero!", frame_display)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    if cv2.waitKey(1) & 0xFF == 27:
        break

face_mesh.close()
cap.release()
cv2.destroyAllWindows()
