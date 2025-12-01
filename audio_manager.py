import pygame

# Inisialisasi mixer Pygame
pygame.mixer.init()

def _play_audio_threaded(path, on_finish=None):
    """Memutar audio di thread terpisah agar tidak memblokir."""
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        if on_finish:
            on_finish()
    except Exception as e:
        print(f"⚠️ Audio gagal diputar: {path} - {e}")


def play_audio(path, block=False, on_finish=None):
    """
    Memutar file audio.
    :param path: Path ke file audio.
    :param block: Jika True, eksekusi akan berhenti hingga audio selesai.
    :param on_finish: Fungsi callback setelah audio selesai (non-blocking).
    """
    if block:
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"⚠️ Audio gagal diputar (blocking): {path} - {e}")
    else:
        # Putar audio di thread terpisah (non-blocking)
        import threading
        thread = threading.Thread(target=_play_audio_threaded, args=(path, on_finish))
        thread.daemon = True  # Thread berhenti jika program utama keluar
        thread.start()


def stop_audio():
    """Menghentikan audio yang sedang diputar."""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"⚠️ Gagal menghentikan audio: {e}")
