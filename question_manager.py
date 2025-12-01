import random

# Database hero (nama, file suara, file gambar)
heroes = [
    {
        "name": "Alucard",
        "voice": "assets/voices/Alucard.mp3",
        "image": "assets/heroes/Alucard.jpg"
    },
    {
        "name": "Angela",
        "voice": "assets/voices/Angela.mp3",
        "image": "assets/heroes/Angela.jpg"
    },
    {
        "name": "Akai",
        "voice": "assets/voices/Akai.mp3",
        "image": "assets/heroes/Akai.jpg"
    },
    {
        "name": "Alpha",
        "voice": "assets/voices/Alpha.mp3",
        "image": "assets/heroes/Alpha.jpg"
    },
    {
        "name": "Argus",
        "voice": "assets/voices/Argus.mp3",
        "image": "assets/heroes/Argus.jpg"
    },
    {
        "name": "Balmond",
        "voice": "assets/voices/Balmond.mp3",
        "image": "assets/heroes/Balmond.jpg"
    },
    {
        "name": "Cecilion",
        "voice": "assets/voices/Cecilion.mp3",
        "image": "assets/heroes/Cecilion.jpg"
    },
    {
        "name": "Karina",
        "voice": "assets/voices/Karina.mp3",
        "image": "assets/heroes/Karina.jpg"
    },
    {
        "name": "Popol Kupa",
        "voice": "assets/voices/Popol Kupa.mp3",
        "image": "assets/heroes/Popol Kupa.jpg"
    },
    {
        "name": "Yuzhong",
        "voice": "assets/voices/Yuzhong.mp3",
        "image": "assets/heroes/Yuzhong.jpg"
    }
]

# Daftar hero yang tersedia untuk pertanyaan, diacak
available_heroes = heroes.copy()
random.shuffle(available_heroes)

def get_question():
    """Mengambil satu soal acak, memastikan tidak ada pengulangan hingga semua hero muncul."""
    global available_heroes
    # Jika hero sudah habis, reset dan acak kembali
    if not available_heroes:
        available_heroes = heroes.copy()
        random.shuffle(available_heroes)

    # Ambil satu hero sebagai jawaban benar
    correct = available_heroes.pop()
    # Ambil hero lain secara acak sebagai jawaban salah
    wrong = random.choice([h for h in heroes if h != correct])

    # Acak posisi pilihan A dan B
    if random.random() > 0.5:
        options = {"A": correct["name"], "B": wrong["name"]}
        correct_answer = "A"
    else:
        options = {"A": wrong["name"], "B": correct["name"]}
        correct_answer = "B"

    return correct, options, correct_answer
