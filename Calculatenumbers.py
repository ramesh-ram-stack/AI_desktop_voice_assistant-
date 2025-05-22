import wolframalpha
import pyttsx3

# Initialize speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def WolfRamAlpha(query):
    """Queries WolframAlpha and returns the answer."""
    apikey = "LPTR7Q-88KKPX8PXV"  # Replace with your actual API key
    client = wolframalpha.Client(apikey)

    try:
        response = client.query(query)
        answer = next(response.results).text
        return answer
    except StopIteration:
        speak("I'm sorry, I couldn't find an answer.")
        return None
    except Exception as e:
        print("Error querying WolframAlpha:", e)
        speak("There was an issue processing your query.")
        return None

def Calc(query):
    """Processes a math query and speaks the result."""
    if not query:
        speak("No query provided.")
        return

    cleaned_query = query.lower().replace("charlie", "").strip()

    # Replace common verbal operators with symbols
    replacements = {
        "multiply by": "*",
        "multiply": "*",
        "times": "*",
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "divide by": "/",
        "divide": "/",
        "over": "/",
    }

    for word, symbol in replacements.items():
        cleaned_query = cleaned_query.replace(word, symbol)

    try:
        result = WolfRamAlpha(cleaned_query)
        if result:
            print(f"Answer: {result}")
            speak(f"The answer is {result}")
        else:
            speak("I couldn't understand the math problem.")
    except Exception as e:
        print("Calculation Error:", e)
        speak("Sorry, something went wrong with the calculation.")


