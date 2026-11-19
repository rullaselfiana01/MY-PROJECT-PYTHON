import random

secret_number = random.randint(1, 10)
guess = 0

while guess != secret_number:
    guess = int(input("Tebak angka 1-10: "))

    if guess > secret_number:
        print("Terlalu besar!")
    elif guess < secret_number:
        print("Terlalu kecil!")
    else:
        print("Benar! Kamu menang!")
