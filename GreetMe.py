import pyttsx3
import datetime

# Initialize TTS engine
engine = pyttsx3.init("sapi5")

# Set voice properties
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Select the first voice
engine.setProperty("rate", 185)  # Speech rate

def speak(text: str) -> None:
    """Speak the given text aloud."""
    engine.say(text)
    engine.runAndWait()

def greetMe() -> None:
    """Greet user based on current time of day."""
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good morning, sir. Wishing you a productive day ahead!")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")

    speak("How can I assist you today?")

if __name__ == "__main__":
    greetMe()
