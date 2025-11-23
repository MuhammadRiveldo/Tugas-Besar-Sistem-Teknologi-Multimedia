import pygame

# Inisialisasi pygame mixer
pygame.mixer.init()

def play_audio(path, block=False):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        if block:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"⚠️ Audio gagal diputar: {path} - {e}")

def stop_audio():
    """Menghentikan pemutaran audio yang sedang berjalan."""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"⚠️ Gagal menghentikan audio: {e}")
