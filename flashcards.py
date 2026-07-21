import tkinter as tk
import random


words = [
    {"English": "Hello", "French": "Bonjour"},
    {"English": "Bread", "French": "Pain"},
    {"English": "Water", "French": "Eau"},
    {"English": "Cat", "French": "Chat"},
]
current_card = {}

def next_card():
    global current_card
    current_card = random.choice(words)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.config(bg="white")

def flip_card():
    canvas.itemconfig(card_title, text="French", fill="white")
    canvas.itemconfig(card_word, text=current_card["French"], fill="white")
    canvas.config(bg="blue")

window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=400, height=260, bg="white", highlightthickness=0)
card_title = canvas.create_text(200, 100, text="Title", font=("Arial", 20, "italic"))
card_word = canvas.create_text(200, 160, text="Word", font=("Arial", 40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


flip_button = tk.Button(text="FLIP", command=flip_card)
flip_button.grid(column=0, row=1)

next_button = tk.Button(text="NEXT CARD", command=next_card)
next_button.grid(column=1, row=1)

# Initialize the first card
next_card()

window.mainloop()
