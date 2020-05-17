import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os, sys, subprocess
import smtplib

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

# This is function is used to open a file depending on what os you are using

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# This function speaks whatever is provided as audio

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# This function greets the user depending on what time it is
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am Jarvis sir, Please tell me how may I help you?")

#it takes microphone input from the user and returns string output

def takeCommand():
    r  = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
    
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"

    return query

# This function helps in sending email please make sure to enter the email and password correctly also make sure that your gmail account has allowed less trusted places

def sendEmail(to,content):
    server = smtplib.SMTP("smtp.email.com",587)
    server.ehlo()
    server.starttls()
    server.login('your_email@email.com','your_password')
    server.sendmail('your_email@email.com',to,content)
    server.close()

if __name__ == "__main__":
    wishMe()
    client = webbrowser.get("open -a /Applications/Google\ Chrome.app %s")
    while True:
        query = takeCommand().lower()

        #Logic for executing tasks based on query


        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            client.open("http://youtube.com")

        elif 'open google' in query:
            client.open("http://google.com")

        elif 'open stackoverflow' in query:
            client.open("http://stackoverflow.com")

        elif 'play music' in query:
            music_dir = "/Users/nikhilmankani/Downloads/songs"
            songs = os.listdir(music_dir)
            print(songs)
            open_file(os.path.join(music_dir,songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")

        elif 'open pages' in query:
            codePath = '/Users/nikhilmankani/Desktop/Visual\ Studio\ Code.app'
            subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/Pages.app"])

        elif 'email to xyz' in query:
            try:
                speak("What should I say")
                content = takeCommand()
                to = "send_to@email.com"
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend I am not able to send this email")
        
        elif 'quit' in query or 'stop' in query:
            exit()
        
        

