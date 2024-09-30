import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import wikipedia
import webbrowser
import random
import time
import pygame


pygame.mixer.init()



def speak(text):
    print(f"Assistant: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)


    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Tick the clock to prevent freezing


    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


    os.remove(filename)


# Wishing based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! How can I assist you today?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! How can I assist you today?")
    else:
        speak("Good Evening! How can I assist you today?")


# Function to take voice input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    except sr.RequestError:
        speak("Sorry, I couldn't reach Google services. Please try again.")
        return "None"

    return query.lower()




# Function to open specific websites
def openWebsite(website_name):
    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://gmail.com",
        "wikipedia": "https://wikipedia.org"
    }
    if website_name in websites:
        speak(f"Opening {website_name} for you.")
        webbrowser.open(websites[website_name])
    else:
        speak(f"Sorry, I don't know how to open {website_name}.")


# Function to give the current time
def getTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")


# Function to fetch information from Wikipedia
def searchWikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except Exception:
        speak("Sorry, I couldn't find information on that.")


# Function to tell a joke
def tellJoke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "How many programmers does it take to change a light bulb? None, it's a hardware problem!"
    ]
    joke = random.choice(jokes)
    speak(joke)


# Function to set a simple reminder
def setReminder(task, delay_in_seconds):
    speak(f"Setting a reminder to {task} in {delay_in_seconds // 60} minutes.")
    time.sleep(delay_in_seconds)
    speak(f"Reminder: It's time to {task}")


# Main driver function
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        if query is None or query == "none":
            continue

        if 'wikipedia' in query:
            searchWikipedia(query)

        elif 'open youtube' in query:
            openWebsite("youtube")

        elif 'open google' in query:
            openWebsite("google")

        elif 'open gmail' in query:
            openWebsite("gmail")

        elif 'play music' in query:
            playMusic()

        elif 'what is the time' in query:
            getTime()

        elif 'tell me a joke' in query:
            tellJoke()

        elif 'set reminder' in query:
            speak("What would you like me to remind you about?")
            task = takeCommand()
            if task != "none":
                speak(f"In how many minutes do you want to be reminded about {task}?")
                try:
                    minutes = int(takeCommand().split()[0])
                    setReminder(task, minutes * 60)
                except ValueError:
                    speak("Sorry, I couldn't understand the time interval.")

        elif   in query or 'exit' in query:
            speak("Goodbye! Have a great day ahead.")
            break
