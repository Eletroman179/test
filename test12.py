import tkinter as tk
import threading
import pyttsx3


def speak(text):
    v = pyttsx3.init()
    v.say(text)
    v.runAndWait()
    v.stop()

def prank():

    text = "Ha ha, you idiot"
    win = tk.Tk()
    win.attributes("-fullscreen", True)
    win.attributes("-topmost", True)
    win.configure(bg="#1e6ae6")

    label = tk.Label(
        win,
        text=text,
        fg="white",
        bg="#1e6ae6",
        font=("Arial", 80)
    )

    label.pack(expand=True) 

    threading.Thread(target=speak, args=(text,), daemon=True).start()

    win.mainloop()

prank()
