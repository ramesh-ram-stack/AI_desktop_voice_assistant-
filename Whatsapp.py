import pywhatkit
import pyttsx3
import speech_recognition as sr
import difflib

# === Voice Engine Setup ===
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Capture voice input and return it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't get that.")
        except sr.RequestError:
            speak("Speech service is currently unavailable.")
        except Exception as e:
            print("Error:", e)
            speak("Something went wrong.")
    return "none"

def get_best_match(recipient, contacts):
    """Return best matching contact name or None."""
    matches = difflib.get_close_matches(recipient, contacts.keys(), n=1, cutoff=0.5)
    if matches:
        return matches[0]
    return None

def sendMessage():
    """Sends a WhatsApp message instantly to a predefined contact."""
    contacts = {
        "person one": "+916361022067",
        "person two": "+918088268700",
    }

    speak("Who do you want to message? Person one or person two?")
    recipient = takeCommand()

    if recipient == "none":
        speak("Sorry, I didn't get the contact name.")
        return

    matched_contact = get_best_match(recipient, contacts)

    if matched_contact:
        speak(f"What message do you want to send to {matched_contact}?")
        message = takeCommand()

        if message != "none" and message.strip() != "":
            speak(f"Sending message to {matched_contact} now.")
            try:
                pywhatkit.sendwhatmsg_instantly(contacts[matched_contact], message, wait_time=10, tab_close=True)
                speak("Message sent successfully.")
            except Exception as e:
                print("Error sending message:", e)
                speak("Sorry, I couldn't send the message.")
        else:
            speak("Message was not understood.")
    else:
        speak("I couldn't find that contact. Please try again.")

# === MAIN ===
if __name__ == "__main__":
    speak("Assistant is ready.")
    while True:
        query = takeCommand()

        if query == "none":
            continue
        elif "send message" in query or "whatsapp" in query:
            sendMessage()
        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
