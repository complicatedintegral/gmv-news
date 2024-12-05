GMV News Application
Overview
The GMV News Application is a Python-based GUI application built using the Tkinter library. It allows users to log in, register, and access news articles from various defense-related websites. Users can read articles, convert them to speech, translate them into different languages, and extract keywords. The application also allows users to save articles to a text file.

Features
User registration and login functionality.
Fetches news articles from multiple defense news websites.
Converts article text to speech using Google Text-to-Speech (gTTS).
Translates articles into different languages using Google Translate.
Extracts and displays keywords from the articles.
Saves articles to a text file.
User-friendly GUI with Tkinter.
Requirements
To run this application, you need to have the following Python packages installed:

tkinter
Pillow (for image handling)
pymysql (for MySQL database connection)
googletrans (for translation)
gtts (for text-to-speech conversion)
rake_nltk (for keyword extraction)
beautifulsoup4 (for web scraping)
requests-html (for making HTTP requests)

You can install the required packages using pip:
pip install Pillow pymysql googletrans gtts rake-nltk beautifulsoup4 requests-html

Database Setup
The application uses a MySQL database to store user credentials. You need to create a database named details and a table named up with the following structure:
CREATE TABLE up (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

Usage
Run the Application: Execute the Python script to launch the application.
Register: Click on the "Register" button to create a new account. Enter a username and password, then click "Submit".
Login: Enter your username and password, then click "Submit" to log in.
Select News Source: After logging in, you can select a news source from the displayed images.
Read Articles: Click on the "Open News" button to view articles. You can:
Convert the article to speech.
Translate the article into a different language.
Display keywords from the article.
Save the article to a text file.
Exit: Click on the "Exit Application" button to close the application.
Code Structure
Imports: The necessary libraries are imported at the beginning of the script.
Database Connection: A connection to the MySQL database is established.
GUI Setup: The Tkinter GUI is set up with various frames, labels, buttons, and text areas.
Functions: Various functions handle registration, login, article fetching, speech conversion, translation, keyword extraction, and file saving.
Main Loop: The application runs in a loop until the user decides to exit.
