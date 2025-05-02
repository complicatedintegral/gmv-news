GMV News Application
GMV News Application is a Python-based desktop app that delivers curated defense news from various websites. With a simple and intuitive GUI built using Tkinter, the app provides users with tools to read, translate, listen to, and extract key insights from articles. It also supports user authentication and article saving.

🔧 Features
✅ User registration and login (with MySQL backend)

🌐 Fetches news articles from multiple defense-related websites

🔊 Converts article text to speech using gTTS

🌍 Translates articles into different languages via Google Translate

🧠 Extracts keywords using RAKE (rake-nltk)

💾 Saves articles to .txt files

🖼️ User-friendly GUI with image-based news source selection

📦 Requirements
Make sure you have the following Python packages installed:

bash/cmd
pip install Pillow pymysql googletrans gtts rake-nltk beautifulsoup4 requests-html

Note: tkinter is included by default with most Python installations. If not, you may need to install it manually depending on your OS.

🗃️ Database Setup
Install and set up MySQL.

Create a database named details.

sql
create database details;
use details;

Within the details database, create a table called up using the following SQL command:

sql
CREATE TABLE up (
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

Ensure your MySQL connection parameters (host, user, password, and database) are correctly configured in your Python script.

🚀 How to Use
Run the Application
Launch the Python script to open the main application window.

Register a New Account
Click "Register", enter a username and password, then click "Submit".

Login
Use your credentials and click "Submit" to log in.

Choose a News Source
After logging in, click on one of the images representing a defense news website.

Read and Interact with Articles

View articles directly in the app

Convert to speech

Translate to different languages

Extract and view keywords

Save the article content to a text file

Exit
Click "Exit Application" to close the app.

🗂️ Code Structure
Imports: Required libraries

Database Connection: Establishes MySQL connection

GUI Setup: Tkinter windows, frames, buttons, and layout

Core Functions:

User registration and login

News scraping and display

Text-to-speech

Translation

Keyword extraction

File saving

Main Loop: Keeps the application running

🛠️ Technologies Used
Python 3.x

Tkinter

MySQL

BeautifulSoup & Requests-HTML (for scraping)

gTTS (Google Text-to-Speech)

googletrans

rake-nltk

📌 Notes
This is a desktop application and requires a MySQL server running locally or remotely.

The translation and TTS features rely on internet access for Google APIs.

Future improvements may include:

Support for more news sources

GUI theming and customization

Encrypted password storage

📄 License
This project is currently for educational use and does not include a formal license. Please contact the author for permissions or contributions.

