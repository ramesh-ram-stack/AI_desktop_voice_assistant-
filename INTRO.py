from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import time
from pygame import mixer

# Initialize pygame mixer
mixer.init()

# Create the main window
root = Tk()
root.geometry("1270x710")
root.title("Charlie - Starting Up")
root.configure(bg="black")
root.overrideredirect(True)  # Hide the window borders

def play_gif():
    root.lift()
    root.attributes("-topmost", True)

    # Load GIF
    gif = Image.open("SciFi_LoaderBlue.gif")
    lbl = Label(root)
    lbl.place(x=0, y=0)

    # Try to play intro sound
    try:
        mixer.music.load("Startup2.mp3")
        mixer.music.play()
    except Exception as e:
        print("[WARNING] Could not play intro sound:", e)

    # Animate GIF frames
    for frame in ImageSequence.Iterator(gif):
        frame = frame.resize((1270, 710))
        img = ImageTk.PhotoImage(frame)
        lbl.config(image=img)
        root.update_idletasks()
        root.update()
        time.sleep(0.04)  # Adjust speed as needed

    root.destroy()

if __name__ == "__main__":
    play_gif()
