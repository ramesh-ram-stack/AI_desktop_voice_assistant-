import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# === Initialize voice engine ===
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Listens for a voice command and returns the transcribed text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=4)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")
        except Exception as e:
            print(f"Error: {e}")
            speak("Something went wrong.")
    return "none"

def searchGoogle(query):
    for word in ["charlie", "google search", "search on google", "google"]:
        query = query.replace(word, "")
    query = query.strip()
    speak(f"Searching Google for {query}")
    pywhatkit.search(query)
    try:
        summary = wikipedia.summary(query, sentences=1)
        speak("According to Wikipedia:")
        speak(summary)
    except Exception:
        speak("No summary available.")

def searchYoutube(query):
    for word in ["charlie", "youtube search", "search on youtube", "youtube"]:
        query = query.replace(word, "")
    query = query.strip()
    speak(f"Searching YouTube for {query}")
    pywhatkit.playonyt(query)
    speak("Playing now.")

def searchWikipedia(query):
    for word in ["charlie", "search wikipedia for", "wikipedia", "search wikipedia"]:
        query = query.replace(word, "")
    query = query.strip()
    speak(f"Searching Wikipedia for {query}")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        print(result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except Exception:
        speak("I couldn't find a result on Wikipedia.")

# === Main Execution ===
if __name__ == "__main__":
    query = takeCommand()
    if query != "none":
        if "google" in query:
            searchGoogle(query)
        elif "youtube" in query:
            searchYoutube(query)
        elif "wikipedia" in query:
            searchWikipedia(query)
        else:
            speak("Please say Google, YouTube, or Wikipedia in your request.")
