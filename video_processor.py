import cv2

def draw_result(frame, hero_img_path):
    """Menampilkan gambar hero di pojok kanan bawah setelah menjawab."""
    h, w, _ = frame.shape

    hero = cv2.imread(hero_img_path)
    hero = cv2.cvtColor(hero, cv2.COLOR_BGR2RGB) # Konversi ke RGB
    hero = cv2.resize(hero, (160,160)) # Ubah ukuran gambar
    
    # Posisi di pojok kanan bawah dengan padding
    y_offset = h - 160 - 20 # 20px padding dari bawah
    x_offset = w - 160 - 20 # 20px padding dari kanan
    frame[y_offset:y_offset+160, x_offset:x_offset+160] = hero

    return frame
