from flask import Flask
import requests
import random
import os
from instagrapi import Client

app = Flask(__name__)

# Instagram login details
USERNAME = "webdev_yasir"
PASSWORD = "Yas78ir19@#"

# API details
API_URL = "https://programming-memes-images.p.rapidapi.com/v1/memes"
HEADERS = {
    "x-rapidapi-host": "programming-memes-images.p.rapidapi.com",
    "x-rapidapi-key": "71188137f4msh6e2c5c6f7479332p1e0f9djsn4c32fce47b0e"
}

# Folder to store downloaded memes
MEMES_FOLDER = "memes/"

# Make sure the memes folder exists
os.makedirs(MEMES_FOLDER, exist_ok=True)

# Random caption pool
CAPTIONS = [
    "🔥 Fresh meme for you! 😂 #CodingLife #ProgrammerHumor",
    "When the code works, but you don’t know why... 🤯💻 #DevLife",
    "Bug fixing level: Sacrificing sleep 💤🐞 #Debugging",
    "Compiling... Compiling... Still Compiling... ⏳😩 #CodingStruggles",
    "404 Brain Not Found 🧠❌ #CodingProblems",
    "Ctrl + C, Ctrl + V = Senior Developer 😂 #DeveloperJokes",
    "Deploying code like... 🚀🤞 #HopeItWorks",
    "When Stack Overflow saves your life again 😆🙌 #CodeLife",
    "Fix one bug, create ten new ones 🔥🐛 #SoftwareDevelopment",
    "Me: Writes perfect code. Compiler: 'Syntax Error' 🤬💀 #CodeFails"
]

def fetch_meme():
    """Fetch a random meme from the API."""
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors
        memes = response.json()
        if memes:
            return random.choice(memes)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching meme: {e}")
        return None

def download_meme(image_url, meme_name):
    """Download the meme image and save it to the memes folder."""
    try:
        img_data = requests.get(image_url, timeout=30)  # Increased timeout
        if img_data.status_code == 200:
            image_path = os.path.join(MEMES_FOLDER, meme_name)
            with open(image_path, "wb") as file:
                file.write(img_data.content)
            return image_path
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def upload_to_instagram(image_path):
    """Upload the meme to Instagram with a random caption."""
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    caption = random.choice(CAPTIONS)  # Pick a random caption
    cl.photo_upload(image_path, caption)

@app.route("/")
def home():
    """Automatically download and upload meme on page load."""
    # First, fetch and download a meme
    meme = fetch_meme()
    if meme:
        meme_image_url = meme["image"]
        meme_name = str(meme["id"]) + ".jpg"  # Convert ID to string and add .jpg
        meme_path = download_meme(meme_image_url, meme_name)
        
        if meme_path:
            # Upload the downloaded meme to Instagram
            upload_to_instagram(meme_path)
            # Optionally, delete the meme after uploading
            os.remove(meme_path)
            return "Meme downloaded and uploaded to Instagram successfully!"
        else:
            return "Failed to download meme."
    else:
        return "Failed to fetch a meme from the API."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
