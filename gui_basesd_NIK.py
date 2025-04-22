import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import os
import openai
import tkinter as tk
import threading

# 🔹 Set up OpenAI key
openai.api_key = "sk-..."  # Replace with your actual API key

# 🔹 TTS Setup
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

# 🔹 GUI Setup
window = tk.Tk()
window.title("NIK – Virtual Assistant")
window.geometry("750x500")
window.resizable(False, False)

# Colors
bg_color = "#0f0f0f"
fg_color = "#00ffd5"
btn_color = "#1f1f1f"
hover_color = "#333333"
accent_color = "#00ff88"

window.configure(bg=bg_color)

# 🔹 Title
title = tk.Label(window, text="NIK", font=("Consolas", 38, "bold"),
                 fg=accent_color, bg=bg_color)
subtitle = tk.Label(window, text="Your Desktop Voice Assistant",
                    font=("Consolas", 14), fg="#999999", bg=bg_color)

title.pack(pady=20)
subtitle.pack(pady=5)

# 🔹 Instruction Label
output_label = tk.Label(window, text="🎤 Click 'Start Listening' and speak...",
                        font=("Consolas", 14), fg=fg_color, bg=bg_color)
output_label.pack(pady=15)

# 🔹 Response Display
response_label = tk.Label(window, text="", font=("Consolas", 12),
                          fg="#dddddd", bg=bg_color, wraplength=600, justify="center")
response_label.pack(pady=10)

# 🔹 Speak and Display Output
def talk(text):
    print("NIK:", text)
    response_label.config(text=f"NIK: {text}")
    engine.say(text)
    engine.runAndWait()

# 🔹 Capture User Voice
def input_instruction():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_label.config(text="🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)
            instruction = recognizer.recognize_google(audio, language="en-IN").lower()
            output_label.config(text=f"🗣 You said: {instruction}")
            return instruction
        except sr.UnknownValueError:
            talk("Sorry, I didn't catch that.")
        except sr.RequestError:
            talk("Speech service is currently unavailable.")
        return None

# 🔹 Ask ChatGPT
def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception:
        return "Unable to connect to ChatGPT right now."

# 🔹 Process User Commands
def process_command():
    instruction = input_instruction()
    if not instruction:
        return

    if "play" in instruction:
        song = instruction.replace("play", "").strip()
        talk(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        now = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {now}")

    elif "date" in instruction:
        today = datetime.datetime.now().strftime("%d %B %Y")
        talk(f"Today's date is {today}")

    elif "how are you" in instruction:
        talk("I'm great! Ready to assist you.")

    elif "what is your name" in instruction:
        talk("I am Nik, your virtual assistant.")

    elif "thank you" in instruction:
        talk("You're welcome!")

    elif any(kw in instruction for kw in ["who is", "what is", "tell me about", "search"]):
        topic = instruction.replace("who is", "").replace("what is", "").replace("tell me about", "").replace("search", "").strip()
        try:
            talk(f"Searching Wikipedia for {topic}")
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=False, redirect=True)
            talk(summary)
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple topics found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find information on that topic.")
        except:
            talk("Wikipedia search failed. Please try again.")

    elif "open google" in instruction:
        webbrowser.open("https://www.google.com")
        talk("Opening Google")

    elif "open youtube" in instruction:
        webbrowser.open("https://www.youtube.com")
        talk("Opening YouTube")

    elif "open wikipedia" in instruction:
        webbrowser.open("https://www.wikipedia.org")
        talk("Opening Wikipedia")

    elif "open notepad" in instruction:
        os.system("notepad.exe")
        talk("Opening Notepad")

    elif "open calculator" in instruction:
        os.system("calc")
        talk("Opening Calculator")

    elif "shutdown" in instruction:
        talk("Shutting down the system.")
        os.system("shutdown /s /t 5")

    elif any(kw in instruction for kw in ["chat with gpt", "chatgpt", "ask gpt"]):

        talk("What would you like to ask ChatGPT?")
        question = input_instruction()
        if question:
            answer = ask_chatgpt(question)
            talk(answer)

    elif "exit" in instruction or "quit" in instruction:
        talk("Goodbye!")
        window.destroy()

    else:
        talk("Sorry, I did not understand that command.")

# 🔹 Threaded Execution to Prevent Freezing
def threaded_run():
    threading.Thread(target=process_command).start()

# 🔹 Button Hover Effects
def on_enter(e):
    start_button['background'] = hover_color

def on_leave(e):
    start_button['background'] = btn_color

# 🔹 Start Button
start_button = tk.Button(window, text="🚀 Start Listening", font=("Consolas", 14, "bold"),
                         bg=btn_color, fg=fg_color, activeforeground="#00FFFF",
                         relief="flat", padx=20, pady=10, command=threaded_run)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)
start_button.pack(pady=25)

# 🔹 Start the GUI Loop
window.mainloop()
