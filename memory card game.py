
import tkinter as tk
from tkinter import ttk, messagebox
import random

# =========================
# GAME SETTINGS
# =========================

app = tk.Tk()
app.title("Memory Card Challenge")
app.geometry("550x680")
app.configure(bg="#1E1B4B")
app.resizable(False, False)

# Daftar gambar kartu
symbols = [
    "🐱", "🐶", "🐼", "🦊", "🐸",
    "🐵", "🐰", "🐻", "🦁", "🐯"
]

# Pengaturan level
levels = {
    "Easy":  {"pairs": 4, "time": 60, "cols": 4},
    "Normal": {"pairs": 8, "time": 90, "cols": 4},
    "Hard":  {"pairs": 10, "time": 120, "cols": 5}
}

# Variabel permainan
cards = []
buttons = []
first_card = None
second_card = None

score = 0
moves = 0
time_left = 60

matched_pairs = 0
game_running = False
checking = False

timer_job = None
flip_job = None


# =========================
# GAME FUNCTIONS
# =========================

def update_display():

    score_label.config(text=f"SCORE: {score}")
    moves_label.config(text=f"MOVES: {moves}")
    timer_label.config(text=f"TIME: {time_left}s")

    level_label.config(
        text=f"PAIRS: {matched_pairs}/{levels[level_var.get()]['pairs']}"
    )


def hide_cards():

    global first_card, second_card, checking

    if not checking:
        return

    buttons[first_card].config(
        text="?",
        bg="#7C3AED",
        state="normal"
    )

    buttons[second_card].config(
        text="?",
        bg="#7C3AED",
        state="normal"
    )

    first_card = None
    second_card = None
    checking = False


def select_card(index):

    global first_card, second_card
    global score, moves, matched_pairs
    global checking, flip_job

    if not game_running or checking:
        return

    # Cegah membuka kartu yang sama
    if index == first_card:
        return

    # Cegah membuka kartu yang sudah cocok
    if buttons[index]["state"] == "disabled":
        return

    # Tampilkan kartu
    buttons[index].config(
        text=cards[index],
        bg="#FACC15",
        fg="#1E1B4B"
    )

    if first_card is None:

        first_card = index

    else:

        second_card = index
        moves += 1

        # Periksa apakah kartu sama
        if cards[first_card] == cards[second_card]:

            buttons[first_card].config(
                bg="#22C55E",
                state="disabled"
            )

            buttons[second_card].config(
                bg="#22C55E",
                state="disabled"
            )

            score += 10
            matched_pairs += 1

            first_card = None
            second_card = None

            if matched_pairs == levels[level_var.get()]["pairs"]:
                update_display()
                end_game(True)
                return

        else:

            # Kartu berbeda, tutup setelah 800 ms
            checking = True

            buttons[first_card].config(state="disabled")
            buttons[second_card].config(state="disabled")

            flip_job = app.after(800, hide_cards)

    update_display()


# =========================
# TIMER
# =========================

def update_timer():

    global time_left, timer_job

    if not game_running:
        return

    time_left -= 1
    update_display()

    if time_left <= 0:
        end_game(False)

    else:
        timer_job = app.after(1000, update_timer)


# =========================
# END GAME
# =========================

def end_game(won):

    global game_running, timer_job, flip_job
    global checking

    game_running = False

    if timer_job is not None:
        app.after_cancel(timer_job)
        timer_job = None

    if flip_job is not None:
        app.after_cancel(flip_job)
        flip_job = None

    checking = False

    for button in buttons:
        button.config(state="disabled")

    if won:

        message_label.config(
            text="CONGRATULATIONS! YOU WIN! 🎉",
            fg="#4ADE80"
        )

        messagebox.showinfo(
            "You Win!",
            f"Great Job!\n\n"
            f"Score: {score}\n"
            f"Moves: {moves}\n"
            f"Time left: {time_left} seconds"
        )

    else:

        message_label.config(
            text="TIME'S UP! GAME OVER!",
            fg="#F87171"
        )

        messagebox.showinfo(
            "Game Over",
            f"Time is over!\n\n"
            f"Your Score: {score}\n"
            f"Matched Pairs: {matched_pairs}"
        )


# =========================
# START GAME
# =========================

def start_game():

    global cards, buttons
    global first_card, second_card
    global score, moves, time_left
    global matched_pairs, game_running
    global checking, timer_job, flip_job

    # Hentikan timer lama
    if timer_job is not None:
        app.after_cancel(timer_job)
        timer_job = None

    if flip_job is not None:
        app.after_cancel(flip_job)
        flip_job = None

    # Reset variabel
    score = 0
    moves = 0
    matched_pairs = 0

    first_card = None
    second_card = None

    checking = False
    game_running = True

    # Ambil pengaturan level
    selected_level = levels[level_var.get()]

    time_left = selected_level["time"]
    total_pairs = selected_level["pairs"]
    columns = selected_level["cols"]

    # Buat kartu secara acak
    cards = symbols[:total_pairs] * 2
    random.shuffle(cards)

    # Hapus papan sebelumnya
    for widget in board.winfo_children():
        widget.destroy()

    buttons = []

    # Membuat tombol kartu
    for i in range(len(cards)):

        button = tk.Button(
            board,
            text="?",
            font=("Arial", 23, "bold"),
            width=5,
            height=2,
            bg="#7C3AED",
            fg="white",
            activebackground="#FACC15",
            relief="raised",
            bd=4,
            command=lambda x=i: select_card(x)
        )

        button.grid(
            row=i // columns,
            column=i % columns,
            padx=5,
            pady=5
        )

        buttons.append(button)

    message_label.config(
        text="FIND ALL MATCHING PAIRS!",
        fg="white"
    )

    update_display()

    # Mulai timer
    timer_job = app.after(1000, update_timer)


# =========================
# HEADER
# =========================

title = tk.Label(
    app,
    text="🧠 MEMORY CARD GAME",
    font=("Arial", 23, "bold"),
    bg="#1E1B4B",
    fg="#FACC15"
)

title.pack(pady=18)

subtitle = tk.Label(
    app,
    text="FIND THE MATCHING PAIRS!",
    font=("Arial", 10, "bold"),
    bg="#1E1B4B",
    fg="white"
)

subtitle.pack()


# =========================
# LEVEL SELECTION
# =========================

level_frame = tk.Frame(
    app,
    bg="#1E1B4B"
)

level_frame.pack(pady=15)

tk.Label(
    level_frame,
    text="SELECT LEVEL:",
    font=("Arial", 11, "bold"),
    bg="#1E1B4B",
    fg="white"
).pack(side="left", padx=8)

level_var = tk.StringVar(value="Easy")

level_menu = ttk.Combobox(
    level_frame,
    textvariable=level_var,
    values=["Easy", "Normal", "Hard"],
    state="readonly",
    width=12
)

level_menu.pack(side="left")


# =========================
# SCORE PANEL
# =========================

panel = tk.Frame(
    app,
    bg="#312E81",
    padx=10,
    pady=12
)

panel.pack(pady=10, padx=20, fill="x")

score_label = tk.Label(
    panel,
    text="SCORE: 0",
    font=("Arial", 12, "bold"),
    bg="#312E81",
    fg="#4ADE80"
)

score_label.pack(side="left", padx=8)

moves_label = tk.Label(
    panel,
    text="MOVES: 0",
    font=("Arial", 12, "bold"),
    bg="#312E81",
    fg="white"
)

moves_label.pack(side="left", padx=8)

timer_label = tk.Label(
    panel,
    text="TIME: 60s",
    font=("Arial", 12, "bold"),
    bg="#312E81",
    fg="#FACC15"
)

timer_label.pack(side="right", padx=8)


level_label = tk.Label(
    app,
    text="PAIRS: 0/4",
    font=("Arial", 11, "bold"),
    bg="#1E1B4B",
    fg="#C4B5FD"
)

level_label.pack(pady=5)


# =========================
# GAME BOARD
# =========================

board = tk.Frame(
    app,
    bg="#1E1B4B"
)

board.pack(pady=15)


# =========================
# MESSAGE
# =========================

message_label = tk.Label(
    app,
    text="SELECT LEVEL AND PRESS START!",
    font=("Arial", 11, "bold"),
    bg="#1E1B4B",
    fg="white"
)

message_label.pack(pady=10)


# =========================
# BUTTONS
# =========================

control_frame = tk.Frame(
    app,
    bg="#1E1B4B"
)

control_frame.pack(pady=10)

start_button = tk.Button(
    control_frame,
    text="▶ START",
    font=("Arial", 12, "bold"),
    width=12,
    bg="#22C55E",
    fg="white",
    command=start_game
)

start_button.grid(row=0, column=0, padx=8)

restart_button = tk.Button(
    control_frame,
    text="↻ RESTART",
    font=("Arial", 12, "bold"),
    width=12,
    bg="#2563EB",
    fg="white",
    command=start_game
)

restart_button.grid(row=0, column=1, padx=8)


# =========================
# INSTRUCTIONS
# =========================

instruction = tk.Label(
    app,
    text="Match two identical cards to earn 10 points!",
    font=("Arial", 10),
    bg="#1E1B4B",
    fg="#C4B5FD"
)

instruction.pack(pady=15)


# =========================
# RUN APPLICATION
# =========================

app.mainloop()
