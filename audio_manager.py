import pygame

# Inisialisasi pygame mixer
pygame.mixer.init()

def _play_audio_threaded(path, on_finish=None):
    """Fungsi internal untuk dijalankan di thread terpisah."""
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
    :param block: Jika True, akan memblokir eksekusi hingga audio selesai.
    :param on_finish: Callback function yang akan dipanggil setelah audio selesai (hanya jika block=False).
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
        # Jalankan di thread terpisah agar tidak memblokir
        import threading
        thread = threading.Thread(target=_play_audio_threaded, args=(path, on_finish))
        thread.daemon = True  # Agar thread berhenti saat program utama keluar
        thread.start()


def stop_audio():
    """Menghentikan pemutaran audio yang sedang berjalan."""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"⚠️ Gagal menghentikan audio: {e}")
