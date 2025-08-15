import tkinter as tk
from tkinter import messagebox
from tkinter import font
from scraper import run_scraper_for_season  
from analyze import analyze_season  

BG_COLOR = "#ebcfcc"
LAYER_COLOR = "#ece4d9"
TEXT_COLOR = "#0D1B2A"

ENTRY_WIDTH = 30

def run_pipeline():
    season = entry.get().strip().lower().replace(" ", "-")    
    if not season:
        messagebox.showwarning("Missing Input", "Please enter a season.")
        return

    try:
        status_label.config(text="Gathering data . . .")
        root.update()
        csv_path = run_scraper_for_season(season)
        status_label.config(text = "Analyzing data . . .")
        analyze_season(csv_path, season)
        status_label.config(text = "Data collected & analyzed")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Something went wrong.")

# root window (initial pop-up)
root = tk.Tk()
root.title("Fashion Trend Analyzer")
root.geometry("350x200")
root.configure(bg = BG_COLOR)
root.resizable(False, False)

# layer (for added color)
frame = tk.Frame(root, bg=LAYER_COLOR, bd=0, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=325, height=175)

# label
title_font = font.Font(family = "Times", size = 17, weight = "bold", slant = "roman")
label = tk.Label(frame, text="Enter Vogue Runway Show", font=title_font, bg = LAYER_COLOR)
label.pack(pady=(15, 10))

# text box
entry = tk.Entry(frame, font=("Helvetica", 12), bg = BG_COLOR , fg=TEXT_COLOR, width=ENTRY_WIDTH, justify="center", relief="flat")
entry.insert(0, "")
entry.pack(pady=5)

button = tk.Button(frame, text="Analyze", font=("Helvetica", 11), bg=BG_COLOR, fg=TEXT_COLOR, width=15, command=run_pipeline, relief="flat")
button.pack(pady=10)

# status label
status_label = tk.Label(frame, text="", bg = LAYER_COLOR)
status_label.pack(pady=5)

root.mainloop()
