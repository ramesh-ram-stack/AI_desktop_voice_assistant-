import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Map spoken app names to system commands or executable names
dictapp = {
    "file explorer": "explorer",   # Changed from "myfiles" to "explorer" for Windows File Explorer
    "command prompt": "cmd",
    "paint": "mspaint",             # Correct executable for Paint is mspaint
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

def openappweb(query):
    speak("Launching, sir.")
    # Clean the query to remove trigger words
    query = query.lower()
    for word in ["open", "charlie", "launch", "please"]:
        query = query.replace(word, "").strip()

    # Check if the query contains a website domain
    if ".com" in query or ".co.in" in query or ".org" in query:
        # Make sure the URL doesn't have spaces
        url = query.replace(" ", "")
        webbrowser.open(f"https://www.{url}")
    else:
        # Try to open apps
        for app in dictapp:
            if app in query:
                # Use os.system to start the app
                os.system(f"start {dictapp[app]}")
                return
        speak("Application not found.")

def closeappweb(query):
    speak("Closing, sir.")
    query = query.lower()

    # Close tabs in browser using hotkeys if requested
    tab_counts = {
        "one tab": 1,
        "1 tab": 1,
        "2 tab": 2,
        "3 tab": 3,
        "4 tab": 4,
        "5 tab": 5
    }

    for key, count in tab_counts.items():
        if key in query:
            for _ in range(count):
                pyautogui.hotkey("ctrl", "w")
                sleep(0.5)
            speak(f"{count} tab{'s' if count > 1 else ''} closed")
            return

    # Otherwise close app by killing process
    for app in dictapp:
        if app in query:
            os.system(f"taskkill /f /im {dictapp[app]}.exe")
            speak(f"{app} closed.")
            return

    speak("No matching application to close found.")

# Example usage
if __name__ == "__main__":
    # Test open and close functions
    openappweb("open chrome")
    sleep(5)
    closeappweb("close chrome")
