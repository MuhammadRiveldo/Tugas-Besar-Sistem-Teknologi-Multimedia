from playsound import playsound

def play_audio(path):
    try:
        playsound(path)
    except:
        print(f"⚠️ Audio gagal diputar: {path}")
