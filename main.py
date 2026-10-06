import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import xml.etree.ElementTree as ET
import musicLibrary
import time
from google import genai

# Gemini SDK Client Setup
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
client = genai.Client(api_key=GEMINI_API_KEY)

recognizer = sr.Recognizer()

def speak(text):
    try:
        print(f"Jarvis: {text}")
        engine = pyttsx3.init('sapi5')
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        pass

def ask_gemini(query):
    query_clean = query.lower().replace("jarvis", "").strip()
    model_name = "gemini-3.8-flash"  # Official active model
    
    # 503 high-demand spikes se bachne ke liye 4 baar retry logic
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"Answer concisely in 2 sentences for voice output: {query_clean}"
            )
            if response and response.text:
                clean_text = response.text.replace('*', '').replace('#', '')
                return clean_text
        except Exception as e:
            print(f"[{model_name}] Server busy, retrying ({attempt + 1}/4)...")
            time.sleep(2)  # 2 second pause server response ke liye
            
    return "Sorry sir, the AI servers are experiencing high demand right now. Please ask again in a moment."

def get_live_news():
    url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    r = requests.get(url)
    if r.status_code == 200:
        root = ET.fromstring(r.content)
        items = root.findall('./channel/item')[:5]
        return [item.find('title').text.split(' - ')[0] for item in items]
    return []

def processCommand(c):
    c_lower = c.lower()
    
    if "open google" in c_lower:
        webbrowser.open("https://www.google.com")
        speak("Opening Google, sir.")
    elif "open facebook" in c_lower:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook, sir.")
    elif "open youtube" in c_lower:
        webbrowser.open("https://www.youtube.com")
        speak("Opening Youtube, sir.")
    elif "open linkedin" in c_lower:
        webbrowser.open("https://www.linkedin.com")
        speak("Opening Linkedin, sir.")
    elif c_lower.startswith("play"):
        parts = c_lower.split(" ")
        song = parts[1] if len(parts) > 1 else ""
        try:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}, sir.")
        except KeyError:
            speak("Song not found, sir.")
    elif "news" in c_lower:
        try:
            speak("Fetching live news headlines, sir...")
            headlines = get_live_news()
            if headlines:
                speak("Here are today's top headlines:")
                for headline in headlines:
                    speak(headline)
            else:
                speak("Sorry sir, I couldn't fetch news right now.")
        except Exception as e:
            speak("Error while fetching news.")
    else:
        print("Thinking with Gemini AI...")
        reply = ask_gemini(c)
        speak(reply)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
            
            print("recognizing...")
            word = r.recognize_google(audio)
            print(f"Aapne bola: {word}")
            
            if "jarvis" in word.lower():
                speak("Ya")
                
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=10)
                    command = r.recognize_google(audio)
                    print(f"Command mili: {command}")
                    processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            continue