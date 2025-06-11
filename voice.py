import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
try:
    api_key = os.getenv("AIzaSyCR50WoXm5gqy26mc2MIXi35yZxRp0OJnc")
    if api_key:
        genai.configure(api_key=api_key)
        print("API Key configured successfully from environment variable.")
    else:
       
        hardcoded_api_key = "AIzaSyCR50WoXm5gqy26mc2MIXi35yZxRp0OJnc"
        if hardcoded_api_key == "AIzaSyCR50WoXm5gqy26mc2MIXi35yZxRp0OJnc":
             print("Warning: Using placeholder API key. Please replace 'YOUR_API_KEY_HERE'.")
             
        genai.configure(api_key=hardcoded_api_key)
        print("API Key configured successfully from hardcoded value.")

except Exception as e:
    print(f"Error configuring Gemini API key: {e}")
    print("Please ensure you have a valid API key configured either via environment variable or directly in the code.")
    exit()


try:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    tts_engine = pyttsx3.init()
    print("Speech Recognition and TTS engines initialized.")
except Exception as e:
    print(f"Error initializing STT/TTS engines: {e}")
    print("Please ensure microphone is connected and audio drivers are working.")
    print("You might need to install PyAudio dependencies (like PortAudio) or TTS engines (like espeak on Linux).")
    exit()

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    print(f"Gemini Model '{model.model_name}' initialized and chat started.")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    exit()
def speak(text):
    """Converts text to speech."""
    print(f"Gemini (speaking): {text}") 
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"Error during speech synthesis: {e}")

def listen_for_input():
    """Listens for audio input and transcribes it."""
    with microphone as source:
        print("\nAdjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15) # Listen for up to 5 secs of silence, max 15 secs phrase
            print("Recognizing...")
            text = recognizer.recognize_google(audio) # Uses Google Web Speech API
            print(f"You (heard): {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within the time limit.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during listening/recognition: {e}")
            return None

speak("Hello! Sanjana voice assistant is ready. How can I help you today?")
while True:
    user_input_text = listen_for_input()
    if user_input_text:
        if user_input_text.lower() in ['quit', 'exit', 'goodbye', 'stop']:
            speak("Goodbye!")
            break
        try:
            speak("Okay, thinking..") 
            
            # Send user input to the Gemini model for a response
            response = chat.send_message(user_input_text)
            
            # Get the response text from Gemini
            response_text = response.text if response else "Sorry, I couldn't get a response from sanjana."

            # Speak the response
            speak(response_text)

        except Exception as e:
            error_message = f"Sorry, an error occurred while communicating with Gemini: {e}"
            print(error_message)
            speak("Sorry, I encountered an error. Please try again.")
    else:
        speak("Did you say something? I didn't catch that. Please try again.")

print("\nAssistant session ended.")
