import cv2

def draw_options(frame, options, score):
    cv2.putText(frame, "Tebak Suara Hero Ini!",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.1, (255,255,255), 3)

    cv2.putText(frame, f"A: {options['A']}",
                (50, 420), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,255,255), 2)

    cv2.putText(frame, f"B: {options['B']}",
                (350, 420), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,255,255), 2)

    cv2.putText(frame, "Move LEFT for A | Move RIGHT for B",
                (60, 470), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255,255,255), 2)

    # Tampilkan skor
    cv2.putText(frame, f"Score: {score}/5",
                (500, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2)

    return frame

def draw_result(frame, hero_img_path, correct=True):
    icon_path = "assets/ui/correct.jpg" if correct else "assets/ui/wrong.jpg"
    icon = cv2.imread(icon_path)

    icon = cv2.resize(icon, (120,120))
    frame[20:140, 20:140] = icon

    hero = cv2.imread(hero_img_path)
    hero = cv2.resize(hero, (320,320))
    frame[100:420, 160:480] = hero

    text = "Correct!" if correct else "Wrong!"
    color = (0,255,0) if correct else (0,0,255)

    cv2.putText(frame, text, (180,470),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)

    return frame

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame, (x, y, w, h)
    
    return frame, None
