import pyttsx3
import datetime
import os
import time as tm  # renamed to avoid conflict with time class

# Initialize TTS engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def read_alarm_time_from_file(file_path="Alarmtext.txt"):
    try:
        with open(file_path, "rt") as f:
            alarm_time = f.read().strip()
        # Clear the file after reading
        with open(file_path, "w") as f:
            f.truncate(0)
        return alarm_time
    except Exception as e:
        speak("Error reading alarm file.")
        print("Error:", e)
        return None

def format_alarm_time(raw_time):
    cleaned = (
        raw_time.lower()
        .replace("charlie", "")
        .replace("set an alarm", "")
        .replace("and", ":")
        .replace(" ", "")
    )
    try:
        return datetime.datetime.strptime(cleaned, "%H:%M:%S").time()
    except ValueError:
        try:
            return datetime.datetime.strptime(cleaned, "%H:%M").time()
        except ValueError:
            return None

def ring_alarm(alarm_time):
    speak(f"Alarm is set for {alarm_time}")
    while True:
        now = datetime.datetime.now().time().replace(microsecond=0)
        if now == alarm_time:
            speak("Alarm ringing now!")
            try:
                if os.path.exists("music.mp3"):
                    os.startfile("music.mp3")
                else:
                    speak("Alarm sound file not found.")
            except Exception as e:
                speak("Couldn't play the alarm sound.")
                print("Error:", e)
            break
        tm.sleep(1)  # Check every second

if __name__ == "__main__":
    raw_time = read_alarm_time_from_file()
    if raw_time:
        alarm = format_alarm_time(raw_time)
        if alarm:
            ring_alarm(alarm)
        else:
            speak("The alarm time format is invalid.")
    else:
        speak("No alarm time found.")
