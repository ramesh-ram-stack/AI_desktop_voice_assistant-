import requests
import pyttsx3
import speech_recognition as sr

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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your response...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=6)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower()
    except:
        print("Could not understand. Please try again.")
        return "none"

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

    speak("Which category of news do you want? Business, Health, Technology, Sports, Entertainment or Science?")
    field = takeCommand()

    if field == "none":
        speak("I didn't catch that. Please try again later.")
        return

    url = apidict.get(field)
    if not url:
        speak("That category is not available. Please choose from Business, Health, Technology, Sports, Entertainment, or Science.")
        return

    try:
        response = requests.get(url)
        news_data = response.json()
        articles = news_data.get("articles", [])

        if not articles:
            speak("Sorry, I couldn't find any news articles.")
            return

        speak("Here are the top headlines.")

        for i, article in enumerate(articles[:10], 1):  # Limit to 10 headlines
            title = article.get("title", "No title available.")
            link = article.get("url", "No URL available.")

            speak(f"News {i}: {title}")
            print(f"{i}. {title}")
            print(f"More: {link}\n")

            speak("Say 'next' to continue or 'stop' to finish.")
            user_input = takeCommand()

            if "stop" in user_input:
                speak("Okay, stopping news.")
                break

        speak("That's all for now.")

    except Exception as e:
        print("Error while fetching news:", e)
        speak("Sorry, I couldn't fetch the news at the moment.")
