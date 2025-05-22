from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

def volumeup(steps=5):
    """Increase system volume by simulating 'volume up' key presses."""
    for _ in range(steps):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown(steps=5):
    """Decrease system volume by simulating 'volume down' key presses."""
    for _ in range(steps):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

if __name__ == "__main__":
    print("Increasing volume by 5 steps")
    volumeup(5)
    sleep(1)
    print("Decreasing volume by 5 steps")
    volumedown(5)
