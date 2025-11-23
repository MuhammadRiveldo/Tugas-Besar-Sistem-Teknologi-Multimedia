from playsound import playsound
from threading import Thread

def play_audio(path):
    try:
        # Jalankan playsound di thread terpisah agar tidak memblokir
        thread = Thread(target=playsound, args=(path,))
        thread.start()
    except Exception as e:
        print(f"⚠️ Audio gagal diputar: {path} - {e}")
