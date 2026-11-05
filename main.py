
import os
import re
import time
import threading
import webbrowser
from datetime import datetime, timedelta
from urllib.parse import quote_plus

import requests
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv


# Load optional settings from the .env file
load_dotenv()

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID", "").strip()

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Store reminders while the program is running
reminders = []
reminder_lock = threading.Lock()

# Prevent reminder alerts from interrupting speech recognition
speech_lock = threading.Lock()


# -------------------------------
# 1. TEXT-TO-SPEECH
# -------------------------------

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    SPEECH_AVAILABLE = True
except Exception as error:
    print("Speech engine could not start:", error)
    engine = None
    SPEECH_AVAILABLE = False


def speak(message):
    """Display and speak a message."""
    print("Assistant:", message)

    if SPEECH_AVAILABLE:
        try:
            with speech_lock:
                engine.say(message)
                engine.runAndWait()
        except Exception as error:
            print("Voice output error:", error)


# -------------------------------
# 2. SPEECH RECOGNITION
# -------------------------------

recognizer = sr.Recognizer()


def listen():
    """Listen to the microphone and return recognised text."""

    try:
        with sr.Microphone() as source:
            print("\nListening... Speak now.")

            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )

            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=8
            )

        # Uses Google's speech recognition service.
        # An internet connection is required.
        command = recognizer.recognize_google(
            audio, language="en-IN"
        )

        print("You said:", command)
        return command.lower().strip()

    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
    except sr.RequestError as error:
        print("Speech recognition network error:", error)
    except AttributeError:
        print("PyAudio is missing. Install SpeechRecognition[audio].")
    except OSError as error:
        print("Microphone error:", error)
    except Exception as error:
        print("Unexpected listening error:", error)

    return ""


# -------------------------------
# 3. WEATHER API
# -------------------------------

def get_weather(city):
    """Find a city and get its current weather."""

    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        )
        response.raise_for_status()

        places = response.json().get("results", [])

        if not places:
            speak("Sorry, I could not find that city.")
            return

        place = places[0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        city_name = place["name"]

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,"
                           "apparent_temperature,wind_speed_10m,"
                           "weather_code",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()

        current = response.json().get("current", {})

        if not current:
            speak("Weather information is not available right now.")
            return

        temperature = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        message = (
            f"In {city_name}, the temperature is "
            f"{temperature} degrees Celsius. "
            f"It feels like {feels_like} degrees. "
            f"Humidity is {humidity} percent, "
            f"and wind speed is {wind} kilometres per hour."
        )

        speak(message)

    except requests.RequestException as error:
        print("Weather API error:", error)
        speak("I could not retrieve weather information.")
    except (ValueError, KeyError, TypeError) as error:
        print("Invalid weather response:", error)
        speak("I received invalid weather data.")


# -------------------------------
# 4. WOLFRAMALPHA API
# -------------------------------

def ask_wolfram(question):
    """Answer a factual question using WolframAlpha."""

    if not WOLFRAM_APP_ID:
        speak(
            "WolframAlpha is not configured yet. "
            "Add your App ID to the .env file."
        )
        return

    try:
        response = requests.get(
            "https://api.wolframalpha.com/v1/result",
            params={
                "appid": WOLFRAM_APP_ID,
                "i": question,
            },
            timeout=15,
        )
        response.raise_for_status()

        answer = response.text.strip()

        if answer:
            speak(answer[:500])
        else:
            speak("I could not find an answer.")

    except requests.RequestException as error:
        print("WolframAlpha API error:", error)
        speak("I could not contact WolframAlpha.")
    except Exception as error:
        print("Question error:", error)
        speak("Sorry, something went wrong.")


# -------------------------------
# 5. REMINDERS
# -------------------------------

def add_reminder(command):
    """
    Example:
    remind me to drink water in 2 minutes
    """

    pattern = (
        r"remind me to (.+?) in (\d+) "
        r"(seconds?|minutes?|hours?)"
    )

    match = re.search(pattern, command)

    if not match:
        speak(
            "Please say, remind me to drink water in 2 minutes."
        )
        return

    task = match.group(1).strip()
    amount = int(match.group(2))
    unit = match.group(3)

    if amount < 1 or amount > 100000:
        speak("Please choose a valid reminder duration.")
        return

    if unit.startswith("second"):
        delay = amount
    elif unit.startswith("minute"):
        delay = amount * 60
    else:
        delay = amount * 3600

    reminder_time = datetime.now() + timedelta(seconds=delay)

    with reminder_lock:
        reminders.append({
            "task": task,
            "time": reminder_time,
        })

    speak(f"Reminder set for {task}.")


def reminder_worker():
    """Check reminders in the background."""

    while True:
        now = datetime.now()
        due_tasks = []

        with reminder_lock:
            remaining = []

            for reminder in reminders:
                if reminder["time"] <= now:
                    due_tasks.append(reminder["task"])
                else:
                    remaining.append(reminder)

            reminders[:] = remaining

        for task in due_tasks:
            speak(f"Reminder: {task}")

        time.sleep(1)


# -------------------------------
# 6. COMMAND HANDLER
# -------------------------------

def handle_command(command):
    """Choose an action based on the recognised command."""

    if not command:
        return True

    # Exit commands
    if any(word in command for word in [
        "exit", "quit", "stop assistant", "goodbye"
    ]):
        speak("Goodbye! Have a great day.")
        return False

    # Greetings
    elif "hello" in command or "hi assistant" in command:
        speak("Hello! How can I help you?")

    # Time
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    # Date
    elif "date" in command or "today" in command:
        today = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {today}.")

    # Weather
    elif "weather" in command:
        city_match = re.search(
            r"(?:weather in|weather at|weather for)\s+(.+)",
            command,
        )

        if city_match:
            city = city_match.group(1).strip()
            get_weather(city)
        else:
            speak("Please say the city, for example, weather in Chennai.")

    # Reminders
    elif "remind me" in command:
        add_reminder(command)

    # Google search
    elif command.startswith("search for "):
        query = command.removeprefix("search for ").strip()
        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" + quote_plus(query)
            )
            speak(f"Searching Google for {query}.")

    # YouTube
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    # Google
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    # WolframAlpha questions
    elif command.startswith("ask "):
        question = command.removeprefix("ask ").strip()
        if question:
            ask_wolfram(question)

    # Basic conversational responses
    elif "your name" in command:
        speak("I am your Python voice assistant.")

    elif "how are you" in command:
        speak("I am doing well. Thanks for asking!")

    elif "help" in command:
        speak(
            "You can ask for the time, date, weather in a city, "
            "search for something, open Google or YouTube, "
            "set a reminder, or ask a WolframAlpha question "
            "by saying ask followed by your question. "
            "Say goodbye to exit."
        )

    else:
        speak(
            "Sorry, I do not know that command. "
            "Say help to hear the available commands."
        )

    return True


# -------------------------------
# 7. MAIN PROGRAM
# -------------------------------

def main():
    print("=" * 45)
    print("       PYTHON VOICE ASSISTANT")
    print("=" * 45)

    speak(
        "Voice assistant started. "
        "Say help to learn the commands."
    )

    # Start the reminder checker
    worker = threading.Thread(
        target=reminder_worker,
        daemon=True,
    )
    worker.start()

    running = True

    try:
        while running:
            command = listen()
            running = handle_command(command)

    except KeyboardInterrupt:
        speak("Assistant stopped.")

    except Exception as error:
        print("Program error:", error)
        speak("An unexpected error occurred.")

    finally:
        print("Voice assistant closed.")


if __name__ == "__main__":
    main()
