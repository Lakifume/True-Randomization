# True-Randomization

A fan project in the form of a Python program that aims to give Bloodstained the randomizer experience it deserves, like what many of the Castlevania games got.

![Screenshot (681)](https://github.com/Lakifume/True-Randomization/assets/56451477/8b532e1b-fd58-4738-bf9f-d58a666eebf6)

Discord: https://discord.gg/nUbFA7MEeU

## How to build from source

Requirements:
* Python 3.12 or higher
* pip 23.2.1 or higher
* Optional: dotnet 8

Steps:
* clone the repo
* run `python.exe -m pip install -r requirements.txt`
* download the latest release
* checkout the commit that matches the version of the downloaded release
* Unzip the contents of the release to the `dist/` folder (create it if missing)
  * The `dist/` folder should at the very least contain the `Tools/`, `MapEdit/`, and `Data/` folders from the release
* run `pyinstaller.exe --onefile --add-data "Bloodstained.ico;." --icon=Bloodstained.ico Randomizer.py`
* optional: view the [UAssetSnippet project](SnippetSrc/README.md) to setup UAssetAPI and UAssetSnippet code snippets