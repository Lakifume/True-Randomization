import json
import os
import time
import requests
import zipfile

with open("Data\\config.json", "r") as file_reader:
    config = json.load(file_reader)

api = requests.get("https://api.github.com/repos/Lakifume/True-Randomization/releases/latest").json()

if api["tag_name"] != config[13]["Value"]["Tag"]:
    print("Downloading...")
    
    url = requests.get(api["assets"][0]["browser_download_url"])
    open("True Randomization.zip", "wb").write(url.content)
    
    print("Extracting...")
    
    with zipfile.ZipFile("True Randomization.zip", 'r') as zip_ref:
        zip_ref.extractall("")
    
    if os.path.isfile("True Randomization.zip"):
        os.remove("True Randomization.zip")
    
    print("Done")
    time.sleep(1)
else:
    print("Already up to date")
    time.sleep(3)