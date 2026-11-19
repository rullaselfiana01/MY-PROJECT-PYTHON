
import tkinter as tk
import random

app = tk.Tk()
app.title("Number Guessing Game")
app.geometry("400x400")
app.configure(bg="#F3E8FF")

secret_number = random.randint(1, 20)
attempts = 0

def check_guess():
    global attempts

    try:
        guess = int(entry.get())
        attempts += 1

        if guess == secret_number:
            result.config(text=f"Correct! You Win!\nAttempts: {attempts}")
        elif guess > secret_number:
            result.config(text="Too High! Try Again.")
        else:
            result.config(text="Too Low! Try Again.")

    except ValueError:
        result.config(text="Please enter a number!")

def new_game():
    global secret_number, attempts

    secret_number = random.randint(1, 20)
    attempts = 0
    entry.delete(0, tk.END)
    result.config(text="Guess a number from 1 to 20!")

tk.Label(app, text="GUESS THE NUMBER",
         font=("Arial", 20, "bold"),
         bg="#F3E8FF").pack(pady=25)

tk.Label(app, text="I'm thinking of a number between 1-20",
         bg="#F3E8FF").pack(pady=10)

entry = tk.Entry(app, font=("Arial", 16), justify="center")
entry.pack(pady=15)

tk.Button(app, text="CHECK GUESS",
          command=check_guess,
          bg="#9333EA", fg="white").pack(pady=10)

result = tk.Label(app, text="Good Luck!",
                  font=("Arial", 12, "bold"),
                  bg="#F3E8FF")
result.pack(pady=20)

tk.Button(app, text="NEW GAME",
          command=new_game).pack()

app.mainloop()
