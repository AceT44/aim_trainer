import tkinter as tk
import time
import random


class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("900x600")
        self.window.title("AIM TRAINER")
        self.window.resizable(False, False)
        self.window.config(
            bg="white"
        )

        self.target = Target(self)
        self.time = Time(self)

        self.start_menu()

    def start_menu(self):
        self.quit_btn = tk.Button(
            self.window,
            text="X",
            font=("Times New Roman", 12),
            bg="white",
            fg="black",
            command=self.quit
        )
        self.quit_btn.pack(anchor="nw", padx=5, pady=5)

        self.start_label = tk.Label(
            self.window,
            text="WELCOME TO AIM TRAINER\n*******************************",
            font=("Times New Roman", 30),
            bg="white",
            fg="black"
        )
        self.start_label.pack(side=tk.TOP, pady=30)

        self.start_btn = tk.Button(
            self.window,
            text="START",
            font=("Times New Roman", 25),
            bg="white",
            fg="black",
            command=self.choose_difficulty
        )
        self.start_btn.pack(side=tk.TOP, pady=30)

    def quit(self):
        self.window.destroy()

    def choose_difficulty(self):
        self.start_label.destroy()
        self.start_btn.destroy()

        self.difficulty_label = tk.Label(
            self.window,
            bg="white",
            fg="black",
            font=("Times New Roman", 20),
            text="Select a difficulty level:"
        )
        self.difficulty_label.pack(side=tk.TOP, pady=30)

        self.easy_btn = tk.Button(
            self.window,
            bg="white",
            fg="black",
            font=("Times New Roman", 16),
            text="EASY",
            command=lambda: self.difficulty("easy"),
            width=10
        )
        self.easy_btn.pack(anchor=tk.CENTER, pady=10)

        self.medium_btn = tk.Button(
            self.window,
            bg="white",
            fg="black",
            font=("Times New Roman", 16),
            text="MEDIUM",
            command=lambda: self.difficulty("medium"),
            width=10
        )
        self.medium_btn.pack(anchor=tk.CENTER, pady=10)

        self.hard_btn = tk.Button(
            self.window,
            bg="white",
            fg="black",
            font=("Times New Roman", 16),
            text="HARD",
            command=lambda: self.difficulty("hard"),
            width=10
        )
        self.hard_btn.pack(anchor=tk.CENTER, pady=10)

    def difficulty(self, difficulty_choice):
        if difficulty_choice == "easy":
            self.max_buttons = 10
        elif difficulty_choice == "medium":
            self.max_buttons = 20
        elif difficulty_choice == "hard":
            self.max_buttons = 30

        self.start_game()

    def start_game(self):
        self.difficulty_label.destroy()
        self.easy_btn.destroy()
        self.medium_btn.destroy()
        self.hard_btn.destroy()

        self.countdown_label = tk.Label(
            self.window,
            font=("Times New Roman", 25),
            bg="white",
            fg="black"
        )
        self.countdown_label.pack(side=tk.TOP, pady=30)

        self.time.countdown()

    def main_game(self):
        self.time.timer()

        self.countdown_label.destroy()

        self.score_label = tk.Label(
            self.window,
            text=f"Score: {self.target.buttons_clicked}",
            font=("Times New Roman", 20),
            bg="white",
            fg="black"
        )
        self.score_label.pack(side=tk.TOP, pady=30)

        self.target.game_logic()

    def end_game(self):
        self.time.calculate_time()

        self.time_label = tk.Label(
            self.window,
            text=f"Time: {self.time.time_elapsed:.2f} secs\nAverage reaction time: {self.time.avg_reaction_time}",
            font=("Times New Roman", 20),
            bg="white",
            fg="black"
        )
        self.time_label.pack(side=tk.BOTTOM, pady=30)

        self.score_label.destroy()

        self.frame = tk.Frame(
            self.window,
            bg="white"
        )
        self.frame.pack()

        self.play_again_label = tk.Label(
            self.frame,
            text="PLAY AGAIN?",
            font=("Times New Roman", 25),
            bg="white",
            fg="black"
        )
        self.play_again_label.grid(row=0, column=0, columnspan=2, pady=30)

        self.play_yes_btn = tk.Button(
            self.frame,
            text="YES",
            font=("Times New Roman", 16),
            bg="white",
            fg="black",
            command=self.play_yes
        )
        self.play_yes_btn.grid(row=1, column=0, pady=30)

        self.play_no_btn = tk.Button(
            self.frame,
            text="NO",
            font=("Times New Roman", 16),
            bg="white",
            fg="black",
            command=self.play_no
        )
        self.play_no_btn.grid(row=1, column=1, pady=30)

        self.change_dif_btn = tk.Button(
            self.frame,
            text="CHANGE DIFFICULTY",
            font=("Times New Roman", 16),
            bg="white",
            fg="black",
            command=self.change_difficulty
        )
        self.change_dif_btn.grid(row=2, column=0, columnspan=2, pady=30)

    def play_yes(self):
        self.time_label.destroy()
        self.frame.destroy()

        self.target = Target(self)
        self.time = Time(self)

        self.start_game()

    def play_no(self):
        self.window.destroy()

    def change_difficulty(self):
        self.time_label.destroy()
        self.frame.destroy()

        self.target = Target(self)
        self.time = Time(self)

        self.choose_difficulty()


class Target:
    def __init__(self, ui):
        self.ui = ui
        self.buttons_clicked = 0

    def game_logic(self):
        self.x_loc = random.randint(0, 800)
        self.y_loc = random.randint(100, 500)

        self.buttons = tk.Button(
            self.ui.window,
            text="CLICK ME",
            font=("Times New Roman", 12),
            bg="white",
            fg="black",
            command=self.button_click
        )
        self.buttons.place(x=self.x_loc, y=self.y_loc)

    def button_click(self):
        self.buttons.destroy()

        self.buttons_clicked += 1
        self.ui.score_label.config(text=f"Score: {self.buttons_clicked}")

        if self.buttons_clicked < self.ui.max_buttons:
            self.game_logic()
        else:
            self.ui.end_game()


class Time:
    def __init__(self, ui):
        self.ui = ui
        self.countdown_time = 3
        self.start_time = None
        self.avg_reaction_time = None

    def countdown(self):
        self.ui.countdown_label.config(text=self.countdown_time)

        if self.countdown_time > 0:
            self.countdown_time -= 1

            self.ui.window.after(1000, self.countdown)
            return
        else:
            self.ui.main_game()

    def timer(self):
        self.start_time = time.time()

    def calculate_time(self):
        self.time_elapsed = time.time() - self.start_time

        self.avg_reaction_time = f"{self.time_elapsed / self.ui.max_buttons:.2f} sec/btn"


app = UI()
app.window.mainloop()
