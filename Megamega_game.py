import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os

# --- File Handling ---
def load_high_score():
    if os.path.exists("megascore.txt"):
        with open("megascore.txt", "r") as f:
            try: return int(f.read())
            except: return 999
    return 999

def save_high_score(score):
    with open("megascore.txt", "w") as f:
        f.write(str(score))

class MegaGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Mega Guessing Game")
        self.root.geometry("450x550")
        
        # State
        self.best_score = load_high_score()
        self.current_theme = "dark"
        self.is_running = False
        self.time_left = 10
        self.guesses = 0
        
        self.themes = {
            "dark": {"bg": "#1e1e1e", "fg": "#ffffff", "accent": "#00ffcc", "btn": "#333333"},
            "light": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d7", "btn": "#f0f0f0"}
        }

        # UI Layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        self.score_lbl = tk.Label(self.main_frame, text=f"Best: {self.best_score if self.best_score < 999 else 'None'}", font=("Courier", 12))
        self.score_lbl.pack(pady=5)

        self.timer_lbl = tk.Label(self.main_frame, text="10s", font=("Arial", 30, "bold"), fg="#ff4444")
        self.timer_lbl.pack(pady=10)

        self.hint_lbl = tk.Label(self.main_frame, text="Press START to begin!", font=("Arial", 10))
        self.hint_lbl.pack(pady=10)

        self.entry = tk.Entry(self.main_frame, font=("Arial", 24), justify="center", state="disabled")
        self.entry.pack(pady=10)

        self.submit_btn = tk.Button(self.main_frame, text="GUESS", command=self.check_guess, state="disabled", font=("Arial", 12, "bold"))
        self.submit_btn.pack(pady=10)

        self.start_btn = tk.Button(self.main_frame, text="START GAME", command=self.start_game, bg="#00ffcc", fg="black")
        self.start_btn.pack(pady=10)

        self.theme_btn = tk.Button(self.main_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(side="bottom", pady=20)

        self.apply_theme()

    def apply_theme(self):
        c = self.themes[self.current_theme]
        self.main_frame.config(bg=c["bg"])
        for widget in [self.score_lbl, self.timer_lbl, self.hint_lbl]:
            widget.config(bg=c["bg"], fg=c["fg"] if widget != self.timer_lbl else "#ff4444")
        self.entry.config(bg=c["btn"], fg=c["fg"], insertbackground=c["fg"])
        self.submit_btn.config(bg=c["accent"], fg="black")
        self.theme_btn.config(bg=c["btn"], fg=c["fg"])

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def start_game(self):
        self.secret_number = random.randint(1, 100)
        self.time_left = 10
        self.guesses = 0
        self.is_running = True
        self.entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.start_btn.config(state="disabled")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.tick()

    def tick(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_lbl.config(text=f"{self.time_left}s")
            winsound.Beep(1000, 50)
            self.root.after(1000, self.tick)
        elif self.time_left == 0:
            self.end_game(False)

    def check_guess(self):
        try:
            val = int(self.entry.get())
            self.guesses += 1
            if val == self.secret_number:
                self.end_game(True)
            else:
                dir = "Too HIGH ⬇️" if val > self.secret_number else "Too LOW ⬆️"
                self.hint_lbl.config(text=dir)
                winsound.PlaySound("SystemDefault", winsound.SND_ALIAS)
            self.entry.delete(0, tk.END)
        except: pass

    def end_game(self, won):
        self.is_running = False
        self.entry.config(state="disabled")
        self.submit_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        
        if won:
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            messagebox.showinfo("Win!", f"Got it in {self.guesses} guesses!")
            if self.guesses < self.best_score:
                self.best_score = self.guesses
                save_high_score(self.best_score)
                self.score_lbl.config(text=f"Best: {self.best_score}")
        else:
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            messagebox.showerror("Lost", f"Time out! It was {self.secret_number}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MegaGuessGame(root)
    root.mainloop()
          
