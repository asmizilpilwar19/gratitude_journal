import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date
import random

# -----------------------
# Cute green theme 🌿
# -----------------------
BG = "#eaf7ea"
CARD = "#d7f0da"
BUTTON = "#7bc47f"
BUTTON_HOVER = "#66b36a"
TEXT = "#2f4f34"
SOIL = "#c49a6c"

FONT_TITLE = ("Comic Sans MS", 18, "bold")
FONT_NORMAL = ("Comic Sans MS", 11)

DATA_FILE = "gratitude_entries.json"


# -----------------------
# Storage
# -----------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------
# Cute Button
# -----------------------
class CuteButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=BUTTON,
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            font=FONT_NORMAL,
            cursor="hand2",
            **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=BUTTON_HOVER))
        self.bind("<Leave>", lambda e: self.config(bg=BUTTON))


# -----------------------
# Main App
# -----------------------
class GardenApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gratitude Garden")
        self.geometry("700x600")
        self.configure(bg=BG)

        self.data = load_data()

        self.build_ui()
        self.draw_garden()

    # -----------------------
    # UI
    # -----------------------
    def build_ui(self):
        tk.Label(
            self,
            text="My Gratitude Garden",
            bg=BG,
            fg=TEXT,
            font=FONT_TITLE
        ).pack(pady=10)

        # Card for entry
        card = tk.Frame(self, bg=CARD, padx=20, pady=20)
        card.pack(fill="x", padx=20)

        tk.Label(card, text="What are you grateful for today?", bg=CARD, fg=TEXT).pack()

        self.entry = tk.Text(card, height=3, font=FONT_NORMAL)
        self.entry.pack(pady=6)

        CuteButton(card, text="Plant Seed 🌱", command=self.add_entry).pack()

        # Garden canvas
        self.canvas = tk.Canvas(self, bg=BG, height=360, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

    # -----------------------
    # Add entry
    # -----------------------
    def add_entry(self):
        today = str(date.today())
        text = self.entry.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Oops", "Write something first 🌿")
            return

        # only one per day
        if any(e["date"] == today for e in self.data):
            messagebox.showinfo("Already planted 🌱", "You already added today’s gratitude!")
            return

        self.data.append({
            "date": today,
            "text": text
        })

        save_data(self.data)

        self.entry.delete("1.0", tk.END)
        self.draw_garden()

    # -----------------------
    # Garden drawing
    # -----------------------
    def draw_garden(self):
        self.canvas.delete("all")

        width = 660
        height = 360

        # soil
        self.canvas.create_rectangle(
            0, height - 80, width, height,
            fill=SOIL, outline=""
        )

        count = len(self.data)

        cols = 8
        spacing_x = width // cols
        spacing_y = 70

        shapes = ["🌱", "🌿", "🌼", "🌸", "🍀"]

        for i in range(count):
            col = i % cols
            row = i // cols

            x = spacing_x * col + 40
            y = height - 90 - row * spacing_y

            emoji = random.choice(shapes)

            self.canvas.create_text(
                x, y,
                text=emoji,
                font=("Arial", 28)
            )

        # little counter
        self.canvas.create_text(
            10, 10,
            anchor="nw",
            text=f"Seeds planted: {count}",
            fill=TEXT,
            font=("Comic Sans MS", 11, "bold")
        )


# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    GardenApp().mainloop()
