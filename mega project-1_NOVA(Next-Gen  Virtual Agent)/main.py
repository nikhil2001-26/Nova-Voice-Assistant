import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import sys

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 2.0)

# Perplexity API details
PPLX_API_KEY = "NA"
PPLX_URL = "https://api.perplexity.ai/chat/completions"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_perplexity(prompt):
    """Send user query to Perplexity and return the response."""
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are Nova, a virtual assistant skilled in general tasks like Alexa or Google Assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(PPLX_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Sorry, I couldn't get a response from Perplexity. Error: {e}"

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open gmail" in c:
        webbrowser.open("https://gmail.com")

    elif c.startswith("play"):
        song = c.split(" ", 1)[1] if len(c.split(" ", 1)) > 1 else None
        if song and song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song} in your library.")
     
    
    else:
        # If command isn't a direct action, ask Perplexity
        answer = ask_perplexity(c)
        speak(answer)
        print("Nova:", answer)

def listen_command(timeout=5, phrase_time_limit=3):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return recognizer.recognize_google(audio)

if __name__ == "__main__":
    speak("Initializing Nova...")
    while True:
        try:
            print("Waiting for wake word...")
            word = listen_command()
            if word.lower() == "nova":
                speak("Yes, I am active.")
                print("Nova active...")

                # Listen for command
                command = listen_command()
                processCommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected. Retrying...")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue
