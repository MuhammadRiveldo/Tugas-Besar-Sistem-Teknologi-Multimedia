import cv2

def draw_result(frame, hero_img_path, correct=True):
    # icon_path = "assets/ui/correct.jpg" if correct else "assets/ui/wrong.jpg"
    # icon = cv2.imread(icon_path)
    # icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB) # Konversi icon ke RGB

    # icon = cv2.resize(icon, (120,120))
    # frame[20:140, 20:140] = icon
    h, w, _ = frame.shape

    hero = cv2.imread(hero_img_path)
    hero = cv2.cvtColor(hero, cv2.COLOR_BGR2RGB) # Konversi hero ke RGB
    hero = cv2.resize(hero, (160,160)) # Perkecil gambar hero
    
    # Posisi baru di pojok kanan bawah
    y_offset = h - 160 - 20 # 20px padding from bottom
    x_offset = w - 160 - 20 # 20px padding from right
    frame[y_offset:y_offset+160, x_offset:x_offset+160] = hero

    # text = "Correct!" if correct else "Wrong!"
    # color = (0,255,0) if correct else (255,0,0) # Warna RGB (Hijau, Merah)

    # cv2.putText(frame, text, (180,470),
    #             cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 4)

    return frame
