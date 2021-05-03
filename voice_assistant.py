import pyttsx3
import speech_recognition as sr

"""Make sure your computer has installed: 
        1. pyaudio (if fails, go search google)
        2. speechrecognition
        3. pyttsx3
        4. pywin32 (if using windows system) """


class voice_assistant:
    def __init__(self):
        pass

    # Make python to speak
    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    # Make python to listen
    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""
            try:
                said = r.recognize_google(audio)
            except Exception as e:
                print("Exception:", str(e))
        return said.lower()
