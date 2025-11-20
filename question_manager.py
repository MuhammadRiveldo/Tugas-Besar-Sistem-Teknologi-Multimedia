import random

heroes = [
    {
        "name": "Alucard",
        "voice": "assets/voices/alucard.mp3",
        "image": "assets/heroes/alucard.png"
    },
    {
        "name": "Lancelot",
        "voice": "assets/voices/lancelot.mp3",
        "image": "assets/heroes/lancelot.png"
    },
    {
        "name": "Fanny",
        "voice": "assets/voices/fanny.mp3",
        "image": "assets/heroes/fanny.png"
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
