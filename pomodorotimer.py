import tkinter as tk
import math
reps=0

WORK_MIN = 0.1
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN =0.1
timer = None

def reset_timer():
    global timer, reps
    window.after_cancel(timer)
    timer = None 
    reps = 0     
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg="black")
    check_marks.config(text="")

def start_timer():
    global reps, timer
    if timer:
        return 

    reps += 1
    
    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Long Break", fg="blue")
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Break", fg="pink")
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg="red")
     

def count_down(count):
    global timer  
    
    count_min = math.floor(count / 60)
    count_sec = count % 60
    
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    
    if count > 0:
       
        timer = window.after(1000, count_down, count - 1)
    else:
        
        timer = None  
        
        start_timer()
        
        
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)
window = tk.Tk()  
window.title("My Pomodoro")
window.config(padx=100, pady=50)

title_label = tk.Label(text="Timer", font=("Arial", 35, "bold"))
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=150, highlightthickness=0)
timer_text = canvas.create_text(100, 75, text="00:00", fill="black", font=("Arial", 35, "bold"))
canvas.grid(column=1, row=1)

check_marks = tk.Label(text="", fg="green")
check_marks.grid(column=1, row=3)

start_button = tk.Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

window.mainloop()
