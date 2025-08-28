**Micro ChatBot**

This project is a desktop chatbot application built using Python's Tkinter for the graphical user interface. The chatbot features a login/signup system with a SQLite database for user authentication and uses a combination of Speech Recognition and Text-to-Speech to provide a conversational experience. The bot's responses are powered by the OpenRouter API, which provides access to various language models.

**Features**

**1. User Authentication:** Secure login and signup functionality with a local SQLite database.

**2. Voice Interaction:** Speak your queries using a microphone and listen to the bot's spoken responses.

**3. Text-to-Speech:** The chatbot speaks its responses aloud, in addition to displaying them.

**4. Chat Interface:** A scrollable, intuitive chat window built with Tkinter.

**5. AI-Powered Responses:** Integrates with the OpenRouter API for intelligent and dynamic conversations.

**Getting Started**

**Prerequisites**

You need to install the required Python libraries. All dependencies are listed in the requirements.txt file.

**1. Clone the Repository:**

    git clone https://github.com/your-username/Tkinter-ChatBot.git
    cd Tkinter-ChatBot

**2. Install Libraries:**

Use pip and the requirements.txt file to install all necessary packages.

    pip install -r requirements.txt

**3. Set up your OpenRouter API Key:**

The code uses an API key to connect to the OpenRouter service. You must obtain your own key and replace the placeholder in the micro-chatbot.py file.

-> Sign up or log in to OpenRouter.ai.
  
-> Go to your dashboard or API key settings to generate a new key.
  
-> In MicroChatBot.py, find the fetchResponse() function and replace the Bearer token with your new key:

    "Authorization": "Bearer YOUR_API_KEY_HERE"

**4. Set up the Database:**

You must run the db-creation.py file first to initialize the user database. This will create a user.db file with a table for storing usernames and passwords.

    python db-creation.py

**5. Run the Main Application:**

Execute the main script to start the chatbot.

    python micro-chatbot.py


**Usage**

1. Launch the Application: Run micro-chatbot.py. The login window will appear.

2. Create an Account: Click the "Create an account" button to open the signup form. Fill in your details and sign up.

3. Log In: Use your newly created credentials to log in.

4. Interact with the ChatBot: Once logged in, the chat window will open. You can type your query in the input box and click "Submit" or click the "Speak" button to use your microphone. The chatbot will respond in the chat window and speak its response aloud.
