
import speech_recognition as sr
import pyttsx3

# Test speaker
engine = pyttsx3.init()
engine.say("Hello Saro! Your voice assistant is ready.")
engine.runAndWait()

# Test microphone
recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Listening... Speak something!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    text = recognizer.recognize_google(audio, language="en-IN")

    print("You said:", text)

except sr.UnknownValueError:
    print("Sorry, I could not understand.")

except sr.RequestError as error:
    print("Internet or recognition error:", error)

except Exception as error:
    print("Error:", error)
