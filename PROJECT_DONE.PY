import openai # type: ignore
import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import datetime
import subprocess
import pywhatkit # type: ignore
import webbrowser
import os
import psutil # type: ignore


openai.api_key = "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"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
recognizer = sr.Recognizer()


def speak(message):
    engine.say(message)
    engine.runAndWait()


def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Clearing background noise...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Waiting for your message...")
        recorded_audio = recognizer.listen(source)
        print('Done recording!')
    return recognizer, recorded_audio


def recognize_speech(recognizer, recorded_audio):
    try:
        print('Printing the message...')
        text = recognizer.recognize_google(recorded_audio, language='en-US')
        print('Your message: {}'.format(text))
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as ex:
        speak(f"Could not request results from Google Speech Recognition service; {ex}")
        return None


def get_gpt3_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as ex:
        return f"Error: {ex}"
    
    
def process_command(command):
    try:
        if 'change voice' in command:
            speak('Changing the voice...')
            change_voice(0) # type: ignore
        elif 'brave' in command:
            speak('Opening Brave browser...')
            program_path = "C:\\Users\\abhin\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Brave.lnk"
            subprocess.Popen([program_path])
        elif 'i have a question' in command:
            speak("Sure, please ask your question.")
            recognizer, recorded_audio = capture_audio()
            user_question = recognize_speech(recognizer, recorded_audio)
            if user_question:
                gpt3_response = get_gpt3_response(user_question)
                if len(gpt3_response) > 50: 
                    print("The response is too long. Here is a summary:")
                    print(gpt3_response[:200])  
                else:
                    speak(gpt3_response)
                    
                    while True:
                        recognizer, recorded_audio = capture_audio()
                        stop_command = recognize_speech(recognizer, recorded_audio)
                        if stop_command and 'stop' in stop_command:
                            speak("Stopping.")
                            break  
                speak("Is there anything else I can assist you with?") 
                
        elif 'close the notepad' in command:
            speak('Closing Notepad...')
            for proc in psutil.process_iter():
                if 'notepad' in proc.name().lower():
                    proc.kill()
            speak('Notepad closed.')
            
        elif 'close powerpoint' in command:
            speak('Closing PowerPoint...')
            for proc in psutil.process_iter():
                if 'powerpnt' in proc.name().lower():
                    proc.kill()
            speak('PowerPoint closed.')
        elif 'close excel' in command:
            speak('Closing Excel...')
            for proc in psutil.process_iter():
                if 'excel' in proc.name().lower():
                    proc.kill()
            speak('Excel closed.')
        # Other commands...
        elif 'notepad' in command:
            print('Opening Notepad...')
            speak('Opening Notepad...')
            program_path = "C:\\Windows\\System32\\notepad.exe"
            subprocess.Popen([program_path])
        elif 'excel' in command:
            print('Opening Excel...')
            speak('Opening Excel...')
            program_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            subprocess.Popen([program_path])

        elif 'explorer' in command:
            print('Opening File Explorer...')
            speak('Opening File Explorer...')
            os.system('start explorer')

        elif 'powerpoint' in command:
            print('Opening PowerPoint...')
            speak('Opening PowerPoint...')
            program_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"  
            subprocess.Popen([program_path])
        
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            print(current_time)
            speak(current_time)
        
        elif 'play' in command:
            print('Searching YouTube...')
            speak('Searching YouTube...')
            pywhatkit.playonyt(command)
        elif 'youtube' in command:
            print('Opening YouTube...')
            speak('Opening YouTube...')
            webbrowser.open('www.youtube.com')
        elif 'i have a question' in command:
            speak("Sure, please ask your question.")
            recognizer, recorded_audio = capture_audio()
            user_question = recognize_speech(recognizer, recorded_audio)
            if user_question:
                # Use GPT-3 for user question
                gpt3_response = get_gpt3_response(user_question)
                print("Voice Verse Response:", gpt3_response)
                speak(gpt3_response)
        
        elif 'bye' in command:
            speak("Goodbye! Have a great day.")
            exit()
        elif 'university name' in command:
            speak("The university name is Sharda University.")
        elif 'faculty name' in command:
            speak("The faculty name is Dr. Kishan.")
        elif 'your name' in command:
            speak("My name is VoiceVerse.")
        elif 'tell me about yourself' in command:
            speak("I am VoiceVerse, a Python-based voice assistant, merging technology and creativity to revolutionize user interactions.")
        elif 'weather' in command:
            # Get weather updates
            weather_response = get_weather() 
            print("Weather Update:", weather_response)
            speak(weather_response)
        elif 'note' in command:
            speak("Sure, what would you like to note?")
            recognizer, recorded_audio = capture_audio()
            note_text = recognize_speech(recognizer, recorded_audio)
            if note_text:
                save_note_to_file(note_text)
                speak("Note saved successfully.")
        else:
            gpt3_response = get_gpt3_response(command)
            print("Voice Verse Response:", gpt3_response)
            speak(gpt3_response)

    except Exception as ex:
        print(f"Error: {ex}")



def save_note_to_file(note_text, file_name="notes.txt"):
    with open(file_name, "a") as file:
        file.write(note_text + "\n")


def main():
    while True:
        try:
            recognizer, recorded_audio = capture_audio()
            user_message = recognize_speech(recognizer, recorded_audio)
            if user_message:
                process_command(user_message)
        except Exception as ex:
            print(f"Error: {ex}")


if __name__ == "__main__":
    main()
