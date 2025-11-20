import random

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
    }
]

def get_question():
    correct = random.choice(heroes)
    wrong = random.choice([h for h in heroes if h != correct])

    # Random posisi benar (A atau B)
    if random.random() > 0.5:
        options = {"A": correct["name"], "B": wrong["name"]}
        correct_answer = "A"
    else:
        options = {"A": wrong["name"], "B": correct["name"]}
        correct_answer = "B"

    return correct, options, correct_answer
