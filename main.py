import os
import pyttsx3
import webbrowser
import pyautogui
import speech_recognition as sr
import wikipedia
import pywhatkit
import datetime
import re
import time as tm
import wolframalpha
import requests
import ctypes
import sys
from pynput.keyboard import Key, Controller
from time import sleep
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from pygame import mixer
from datetime import timedelta
import matplotlib.pyplot as plt

# === VOICE SETUP ===
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)
keyboard = Controller()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# === SPLASH SCREEN ===
def play_intro():
    mixer.init()
    intro = Tk()
    intro.geometry("1270x710")
    intro.title("Charlie - Starting Up")
    intro.configure(bg="black")
    intro.overrideredirect(True)

    try:
        gif = Image.open("SciFi_LoaderBlue.gif")
        lbl = Label(intro)
        lbl.place(x=0, y=0)
        mixer.music.load("Startup2.mp3")
        mixer.music.play()

        def animate(counter=0):
            try:
                frame = ImageTk.PhotoImage(gif.copy().resize((1270, 710)))
                lbl.config(image=frame)
                lbl.image = frame
                intro.update_idletasks()
                intro.update()
                gif.seek(counter)
                intro.after(50, animate, counter+1)
            except EOFError:
                intro.destroy()

        animate()
        intro.mainloop()
    except Exception as e:
        print("Splash screen failed:", e)

def greetMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir. Wishing you a productive day ahead!")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("How can I assist you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.energy_threshold = 400
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return "none"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except:
        return "none"

dictapp = {
    "fileexplorer": "explorer",
    "commandprompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

def openappweb(query):
    speak("Launching, sir.")
    query_clean = query.replace("open", "").replace("charlie", "").replace("launch", "").strip()
    if ".com" in query_clean or ".org" in query_clean:
        webbrowser.open("https://www." + query_clean)
    else:
        for app in dictapp:
            if app in query_clean:
                os.system(f"start {dictapp[app]}")
                speak(f"Opening {app}")
                return
        speak("Application not recognized.")

def closeappweb(query):
    speak("Closing, sir.")
    query_clean = query.replace("close", "").replace("charlie", "").strip()
    for app in dictapp:
        if app in query_clean:
            os.system(f"taskkill /f /im {dictapp[app]}.exe")
            speak(f"Closed {app}")
            return
    speak("Application not recognized.")

def searchGoogle(query):
    speak("Searching on Google.")
    query = query.replace("google", "")
    pywhatkit.search(query)
    try:
        summary = wikipedia.summary(query, sentences=1)
        speak(summary)
    except:
        pass

def searchYoutube(query):
    speak("Playing on YouTube.")
    query = query.replace("youtube", "").replace("play", "")
    pywhatkit.playonyt(query)

def searchWikipedia(query):
    query = query.replace("wikipedia", "")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia...")
        speak(result)
    except:
        speak("No Wikipedia result found.")

def setAlarm(query):
    speak("Setting alarm...")
    time_match = re.search(r'(\d{1,2})\s*(hours|hour)?\s*(\d{1,2})?\s*(minutes|minute)?\s*(\d{1,2})?\s*(seconds|second)?', query)
    if time_match:
        h = int(time_match.group(1)) if time_match.group(1) else 0
        m = int(time_match.group(3)) if time_match.group(3) else 0
        s = int(time_match.group(5)) if time_match.group(5) else 0
        now = datetime.datetime.now()
        alarm_time = (now + datetime.timedelta(hours=h, minutes=m, seconds=s)).time().replace(microsecond=0)
    else:
        speak("Couldn't understand the time format.")
        return

    speak(f"Alarm set for {alarm_time.strftime('%H:%M:%S')}")
    while True:
        now = datetime.datetime.now().time().replace(microsecond=0)
        if now == alarm_time:
            speak("Alarm ringing!")
            try:
                os.startfile("music.mp3")
            except:
                speak("Alarm sound not found.")
            break
        tm.sleep(1)

def volumeup(steps=5):
    for _ in range(steps):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown(steps=5):
    for _ in range(steps):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def WolfRamAlpha(query):
    apikey = "LPTR7Q-88KKPX8PXV"
    client = wolframalpha.Client(apikey)
    try:
        response = client.query(query)
        answer = next(response.results).text
        return answer
    except:
        return None

def Calc(query):
    cleaned_query = query.lower().replace("charlie", "").strip()
    replacements = {
        "multiply by": "*", "multiply": "*", "times": "*",
        "plus": "+", "add": "+",
        "minus": "-", "subtract": "-",
        "divide by": "/", "divide": "/", "over": "/"
    }
    for word, symbol in replacements.items():
        cleaned_query = cleaned_query.replace(word, symbol)
    result = WolfRamAlpha(cleaned_query)
    if result:
        speak(f"The answer is {result}")
    else:
        speak("Sorry, I couldn't solve that.")

def latestnews():
    API_KEY = "77eb0e521afa4a4fa0190493a09c1aad"
    apidict = {
        "business": f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={API_KEY}",
        "entertainment": f"https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey={API_KEY}",
        "health": f"https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey={API_KEY}",
        "science": f"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey={API_KEY}",
        "sports": f"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey={API_KEY}",
        "technology": f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={API_KEY}"
    }
    speak("Which category of news would you like?")
    field = takeCommand()
    if field == "none":
        speak("I didn't catch that.")
        return
    url = apidict.get(field)
    if not url:
        speak("Invalid category.")
        return
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        if not articles:
            speak("No news articles found.")
            return
        for article in articles[:5]:
            speak(article.get("title", "No title"))
            sleep(1)
    except:
        speak("Sorry, I couldn't fetch the news.")

def sendMessage():
    contacts = {
        "person one": "+918088268700",
        "person two": "+918088012776"
    }
    speak("Who do you want to message?")
    recipient = takeCommand()
    if recipient in contacts:
        speak("What message should I send?")
        message = takeCommand()
        if message != "none":
            now = datetime.datetime.now()
            send_time = now + timedelta(minutes=2)
            pywhatkit.sendwhatmsg(contacts[recipient], message, send_time.hour, send_time.minute)
            speak("Message scheduled.")
        else:
            speak("Message was not understood.")
    else:
        speak("Contact not found.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def focus_mode():
    speak("Tell me the focus end time, like 14 30 for 2:30 PM.")
    end_time_str = takeCommand()
    if end_time_str == "none":
        speak("I didn't catch that.")
        return

    try:
        hour, minute = map(int, end_time_str.split())
        Stop_Time = f"{hour:02d}:{minute:02d}"
    except:
        speak("Please say the time like '14 30'.")
        return

    start = float(datetime.datetime.now().strftime("%H.%M"))
    end = float(Stop_Time.replace(":", "."))
    focus_duration = round(end - start, 3)

    host_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    redirect = "127.0.0.1"
    sites = ["www.facebook.com", "facebook.com", "www.instagram.com", "instagram.com", "www.youtube.com", "youtube.com"]

    try:
        with open(host_path, "r+") as file:
            content = file.read()
            for site in sites:
                if f"{redirect} {site}" not in content:
                    file.write(f"{redirect} {site}\n")
    except PermissionError:
        speak("Admin rights required.")
        return

    speak(f"Focus Mode activated until {Stop_Time}.")
    while True:
        if datetime.datetime.now().strftime("%H:%M") >= Stop_Time:
            with open(host_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not any(site in line for site in sites):
                        file.write(line)
                file.truncate()
            with open("focus.txt", "a") as f:
                f.write(f"Focus session: {focus_duration} hours\n")
            speak("Focus time over. Websites unblocked.")
            break
        tm.sleep(10)

def focus_graph():
    try:
        with open("focus.txt", "r") as file:
            lines = file.readlines()
        durations = []
        for line in lines:
            match = re.search(r'([\d.]+)', line)
            if match:
                durations.append(float(match.group(1)))
        if not durations:
            speak("No focus data found.")
            return
        x = list(range(1, len(durations)+1))
        plt.figure(figsize=(10, 5))
        plt.plot(x, durations, marker='o', color='blue')
        plt.title("Your Focused Time Sessions")
        plt.xlabel("Session Number")
        plt.ylabel("Focus Time (in hours)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        speak("Focus data not found.")
    except Exception as e:
        speak(f"Error displaying focus graph: {str(e)}")

# === MAIN LOOP ===
if __name__ == "__main__":
    play_intro()
    greetMe()
    speak("Hello! I am ready.")
    while True:
        query = takeCommand()
        if query == "none":
            continue
        if "wake up" in query or "start" in query:
            speak("Activated.")
            while True:
                query = takeCommand()
                if query == "none":
                    continue
                if "sleep" in query or "stop" in query:
                    speak("Powering down. Goodbye.")
                    break
                elif "focus mode" in query:
                    if is_admin():
                        focus_mode()
                    else:
                        speak("Requesting admin access...")
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                        break
                elif "show focus graph" in query or "display focus graph" in query:
                    focus_graph()
                elif "send message" in query or "whatsapp" in query:
                    sendMessage()
                elif "open" in query or "launch" in query:
                    openappweb(query)
                elif "close" in query:
                    closeappweb(query)
                elif "youtube" in query and "play" in query:
                    searchYoutube(query)
                elif "google" in query:
                    searchGoogle(query)
                elif "wikipedia" in query:
                    searchWikipedia(query)
                elif "set alarm" in query:
                    setAlarm(query)
                elif "volume up" in query:
                    volumeup()
                    speak("Volume increased.")
                elif "volume down" in query:
                    volumedown()
                    speak("Volume decreased.")
                elif "calculate" in query or "what is" in query or "solve" in query:
                    Calc(query)
                elif "news" in query:
                    latestnews()
                elif "exit" in query or "quit" in query:
                    speak("Goodbye.")
                    exit()
