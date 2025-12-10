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
    },
    {
        "name": "Hilda",
        "voice": "assets/voices/Hilda.mp3",
        "image": "assets/heroes/Hilda.jpg"
    },
    {
        "name": "Franco",
        "voice": "assets/voices/Franco.mp3",
        "image": "assets/heroes/Franco.jpg"
    },
    {
        "name": "Belerick",
        "voice": "assets/voices/Belerick.mp3",
        "image": "assets/heroes/Belerick.jpg"
    },
    {
        "name": "Granger",
        "voice": "assets/voices/Granger.mp3",
        "image": "assets/heroes/Granger.jpg"
    },
    {
        "name": "Clint",
        "voice": "assets/voices/Clint.mp3",
        "image": "assets/heroes/Clint.jpg"
    },
    {
        "name": "Chang'e",
        "voice": "assets/voices/Chang'e.mp3",
        "image": "assets/heroes/Chang'e.jpg"
    },
    {
        "name": "Estes",
        "voice": "assets/voices/Estes.mp3",
        "image": "assets/heroes/Estes.jpg"
    },
    {
        "name": "Chou",
        "voice": "assets/voices/Chou.mp3",
        "image": "assets/heroes/Chou.jpg"
    },
    {
        "name": "Floryn",
        "voice": "assets/voices/Floryn.mp3",
        "image": "assets/heroes/Floryn.jpg"
    },
    {
        "name": "Lapu lapu",
        "voice": "assets/voices/Lapu lapu.mp3",
        "image": "assets/heroes/Lapu lapu.jpg"
    },
    {
        "name": "Helcurt",
        "voice": "assets/voices/Helcurt.mp3",
        "image": "assets/heroes/Helcurt.jpg"
    },
    {
        "name": "Lancelot",
        "voice": "assets/voices/Lancelot.mp3",
        "image": "assets/heroes/Lancelot.jpg"
    },
    {
        "name": "Gord",
        "voice": "assets/voices/Gord.mp3",
        "image": "assets/heroes/Gord.jpg"
    },
    {
        "name": "Bane",
        "voice": "assets/voices/Bane.mp3",
        "image": "assets/heroes/Bane.jpg"
    },
    {
        "name": "Eudora",
        "voice": "assets/voices/Eudora.mp3",
        "image": "assets/heroes/Eudora.jpg"
    },
    {
        "name": "Layla",
        "voice": "assets/voices/Layla.mp3",
        "image": "assets/heroes/Layla.jpg"
    },
    {
        "name": "Ling",
        "voice": "assets/voices/Ling.mp3",
        "image": "assets/heroes/Ling.jpg"
    },
    {
        "name": "Lolita",
        "voice": "assets/voices/Lolita.mp3",
        "image": "assets/heroes/Lolita.jpg"
    },
    {
        "name": "Minotaur",
        "voice": "assets/voices/Minotaur.mp3",
        "image": "assets/heroes/Minotaur.jpg"
    },
    {
        "name": "Mathilda",
        "voice": "assets/voices/Mathilda.mp3",
        "image": "assets/heroes/Mathilda.jpg"
    },
    {
        "name": "Miya",
        "voice": "assets/voices/Miya.mp3",
        "image": "assets/heroes/Miya.jpg"
    },
    {
        "name": "Moskov",
        "voice": "assets/voices/Moskov.mp3",
        "image": "assets/heroes/Moskov.jpg"
    },
    {
        "name": "Nana",
        "voice": "assets/voices/Nana.mp3",
        "image": "assets/heroes/Nana.jpg"
    },
    {
        "name": "Odette",
        "voice": "assets/voices/Odette.mp3",
        "image": "assets/heroes/Odette.jpg"
    },
    {
        "name": "Rafaela",
        "voice": "assets/voices/Rafaela.mp3",
        "image": "assets/heroes/Rafaela.jpg"
    },
    {
        "name": "Saber",
        "voice": "assets/voices/Saber.mp3",
        "image": "assets/heroes/Saber.jpg"
    },
    {
        "name": "Selena",
        "voice": "assets/voices/Selena.mp3",
        "image": "assets/heroes/Selena.jpg"
    },
    {
        "name": "Sun",
        "voice": "assets/voices/Sun.mp3",
        "image": "assets/heroes/Sun.jpg"
    },
    {
        "name": "Thamuz",
        "voice": "assets/voices/Thamuz.mp3",
        "image": "assets/heroes/Thamuz.jpg"
    },
    {
        "name": "Zilong",
        "voice": "assets/voices/Zilong.mp3",
        "image": "assets/heroes/Zilong.jpg"
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
