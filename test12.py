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
    threading.Thread(target=speak, args=(text,), daemon=True).start()

prank()
