import tkinter as tk
from tkinter import messagebox
import threading
import sqlite3
import requests as req
import pyaudio
import speech_recognition as sr
import pyttsx3 as tts
from tkinter import *


#Verify Credentials
def VerifyCredentials():
    username = nameentry.get()
    password = passwordentry.get()

    # Check credentials in database
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        openChatBot(username)
    else:
        messagebox.showerror("Error", "Invalid username or password!")

#Signup form
def Signup():
    global  nameentry, passwordentry, confirmentry
    signup_window = tk.Toplevel(root)
    signup_window.geometry("1000x600")
    signup_window.minsize(1000, 600)
    signup_window.maxsize(1000, 600)
    signup_window.title("Micro Chatbot - Signup")
    
    
    # Title for Signup
    title_label = tk.Label(signup_window, text="Micro Chatbot Signup!", font=("Arial", 25, "bold"), fg="#e0e0e0", bg="#121212")
    title_label.pack(pady=10, fill="x")
    
    # Frame for Signup form
    frame = tk.Frame(signup_window, bg="#262626", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=200)
    
    # Username label and entry
    name_label = tk.Label(frame, text="Username:", font="Montserrat 10 bold", bg="#262626", fg="#e0e0e0")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    nameentry = tk.Entry(frame, font=("Arial", 12),  bg="#1e1e1e", fg="#e0e0e0")
    nameentry.grid(row=0, column=1, padx=10, pady=10)
    
    # Password label and entry
    password_label = tk.Label(frame, text="Password:", font="Montserrat 10 bold", bg="#262626", fg="#e0e0e0")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    passwordentry = tk.Entry(frame, font=("Arial", 12), show="*",  bg="#1e1e1e", fg="#e0e0e0")
    passwordentry.grid(row=1, column=1, padx=10, pady=10)
    
    # Confirm password label and entry
    confirm_label = tk.Label(frame, text="Confirm Password:", font="Montserrat 10 bold", bg="#262626", fg="#e0e0e0")
    confirm_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    confirmentry = tk.Entry(frame, font=("Arial", 12), show="*", bg="#1e1e1e", fg="#e0e0e0")
    confirmentry.grid(row=2, column=1, padx=10, pady=10)
    
    # Signup button in Signup window
    signup_btn = tk.Button(frame, text="Sign Up", font=("Arial", 12, "bold"),
                           bg="#512da4", fg="#e0e0e0", activebackground="#2b1759", width=30, command=StoreCredentials)
    signup_btn.grid(row=3, column=0, columnspan=2, pady=(20, 0), padx=17)
    signup_window.config(bg="#121212")


#Function to store credentials in DB
def StoreCredentials():
    username = nameentry.get()
    password = passwordentry.get()
    confirm_password = confirmentry.get()

    if not username or not password or not confirm_password:
        messagebox.showwarning("Sign Up", "Please fill in all fields!")
        return

    if password != confirm_password:
        messagebox.showerror("Sign Up", "Passwords do not match!")
        return

    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    finally:
        conn.close()
        messagebox.showinfo("Success", "Signup successful! Please login.")



def openChatBot(username):
    # Function to Speak Response
    def speakResponse(response):
        def speak():
            engine = tts.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)  # Female voice
            engine.say(response)
            engine.runAndWait()
        # Run the speak function in a separate thread to prevent blocking
        threading.Thread(target=speak).start()
    
    global userInput, chatCanvas, chatWindow, rowNum
    
    rowNum = 0 

    # GUI setup
    chat = tk.Toplevel(root)
    chat.title("Micro ChatBot")
    chat.geometry("1200x650")
    chat.minsize(1200, 650)
    chat.maxsize(1200, 650)

    # Welcome label
    welcomeLabel = Label(chat, text=f"Welcome {username} to Micro Chatbot!", font="Poppins 15 bold", pady=15 , fg="#e0e0e0", bg="#121212")
    welcomeLabel.grid(row=0, column=1)
    creators = Label(chat, text="A project created by Ilsa & Sommy", font="Poppins 11 bold", pady=5, fg="#e0e0e0", bg="#121212")
    creators.grid(row=1, column=1)

    # Scrollable Chat Window
    frameContainer = Frame(chat, width=900, height=450)
    frameContainer.grid(row=2, column=1, padx=130, pady=10)

    # Canvas within the frame
    chatCanvas = Canvas(frameContainer, width=900, height=450, bg="#242424", borderwidth=2)
    chatCanvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Add a scrollbar to the frame
    scrollbar = Scrollbar(frameContainer, orient="vertical", command=chatCanvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure canvas to work with scrollbar
    chatCanvas.configure(yscrollcommand=scrollbar.set)
    chatCanvas.bind('<Configure>', lambda e: chatCanvas.configure(scrollregion=chatCanvas.bbox("all")))

    # Add a frame inside the canvas to hold chat messages
    chatWindow = Frame(chatCanvas, background="#242424")
    chatCanvas.create_window((0, 0), window=chatWindow, anchor="nw")

    # Frame for input field and buttons
    inputFrame = Frame(chat, bg="#1e1e1e", bd=2, relief="solid", borderwidth=2)
    inputFrame.grid(row=3, column=1, pady=10, padx=(0,10))

    
    userInput = Entry(inputFrame, width=92, font="Arial 12", bg="#1e1e1e", fg="#e0e0e0")
    userInput.grid(row=0, column=0, padx=(0,5))
    # Function to update the scroll region dynamically
    def updateScrollRegion():
        chatCanvas.update_idletasks()
        chatCanvas.configure(scrollregion=chatCanvas.bbox("all"))

    # Function to auto-scroll to the bottom when new messages are added
    def scrollToBottom():
        chatCanvas.yview_moveto(1.0)

    # Variable to store user query
    query = ""
    # Speech Recognition function to get the query
    def speakQuery():
        global query
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            userInput.delete(0, END)  # Clear the input field before listening
            userInput.insert(0, "Listening...")
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio)
                userInput.delete(0, END)
                userInput.insert(0, query)  # Show the query in input field
                print(f"You said: {query}")
            except sr.UnknownValueError:
                speakResponse("Sorry, I could not understand your voice")
            except sr.RequestError:
                speakResponse("Sorry, the speech service is down")
                
    
    # Function to fetch bot's response
    def fetchResponse():
        userQuery = userInput.get()
        if not userQuery.strip():
            speakResponse("Please provide a query")
            return "Please provide a query"
        
        # OpenAI API URL
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY_HERE",
            "Content-Type": "application/json"
        }

        # Request payload
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": userQuery}]
        }

        try:
            # Make the POST request
            response = req.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except req.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Request failed"


    # Function to display the user query and bot response in the chat window
    def showText():
        global rowNum
        
        queryText = userInput.get() 
        if queryText.strip():  # Check if input is not empty
            userQuery = Label(chatWindow, text=f"You: {queryText}", font="Arial 12", anchor="e", background="#512da4", fg="#e0e0e0", wraplength=250, justify="left", padx=5, pady=5)
            userQuery.grid(row=rowNum, column=1, padx=(50, 10), pady=5, sticky="e")
            
            # Increment row number for the next message
            rowNum += 1
            
            # Fetch the bot's response
            botResponse = fetchResponse()
            
            # Display the bot's response in the GUI
            botResponseLabel = Label(chatWindow, text=f"Micro: {botResponse}", font="Arial 12", anchor="w", background="#595959", fg="#e0e0e0",wraplength=500, justify="left", padx=5, pady=5)
            botResponseLabel.grid(row=rowNum, column=0, padx=(10, 50), pady=5, sticky="w")
            
            # Increment row number after bot response
            rowNum += 1

            # Update the GUI
            updateScrollRegion()
            scrollToBottom()  # Call auto-scroll function

            # Speak the bot's response after displaying it
            if botResponse:
                speakResponse(botResponse)

        # Clear the input field
        userInput.delete(0, END)

    sendIcon = PhotoImage(file="chevron.png")
    microIcon = PhotoImage(file="microphone.png")

    # Submit button
    sendBtn = Button(inputFrame, text="Submit", image=sendIcon, font="Arial 10 bold", bg="#512da8", activebackground="#2b1759", command=showText)
    sendBtn.grid(row=0, column=1, padx=5)

    # Speak button
    speakBtn = Button(inputFrame, text="Speak", image=microIcon, font="Arial 10 bold", bg="#512da8", activebackground="#2b1759", command=speakQuery)
    speakBtn.grid(row=0, column=2, padx=5)

    chat.config(bg="#121212")
    chat.mainloop()


# Root window setup for Login form
root = tk.Tk()
root.geometry("1000x600")
root.minsize(1000, 600)
root.maxsize(1000, 600)
root.title("Micro Chatbot - Login")

# Title for Login form
title_label = tk.Label(root, text="Micro Chatbot Login!", font=("Arial", 25, "bold"), fg="#e0e0e0", bg="#121212")
title_label.pack(pady=10)

# Frame for Login form
frame = tk.Frame(root, bg="#262626", bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=200)

# Username label and entry
name_label = tk.Label(frame, text="Username:", font="Montserrat 10 bold", bg="#262626", fg="#e0e0e0")
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
nameentry = tk.Entry(frame, font=("Arial", 12), bg="#1e1e1e", fg="#e0e0e0")
nameentry.grid(row=0, column=1, padx=10, pady=10)

# Password label and entry
password_label = tk.Label(frame, text="Password:", font="Montserrat 10 bold", bg="#262626", fg="#e0e0e0")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
passwordentry = tk.Entry(frame, font=("Arial", 12), show="*", bg="#1e1e1e", fg="#e0e0e0")
passwordentry.grid(row=1, column=1, padx=10, pady=10)

# Login button
login = tk.Button(frame, text="Login", font=("Arial", 12, "bold"),
                  bg="#512da8", fg="#e0e0e0", activebackground="#2b1759", activeforeground="#e0e0e0", width=30,command=VerifyCredentials)
login.grid(row=3, column=0, columnspan=2, pady=(10, 5), padx=17)

# Signup button
signup = tk.Button(frame, text="Create an account", font=("Arial", 12, "bold"),
                   bg="#512da8", fg="#e0e0e0", activebackground="#2b1759", activeforeground="#e0e0e0", width=30,command=Signup)
signup.grid(row=4, column=0, columnspan=2, pady=5, padx=17)
root.config(bg="#121212")
# Main loop
root.mainloop()
