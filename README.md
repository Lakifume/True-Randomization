# True-Randomization

A fan project in the form of a Python program that aims to give Bloodstained the randomizer experience it deserves, like what many of the Castlevania games got.

![Screenshot (681)](https://github.com/Lakifume/True-Randomization/assets/56451477/8b532e1b-fd58-4738-bf9f-d58a666eebf6)

Discord: https://discord.gg/nUbFA7MEeU

## How to build from source

Requirements:
* latest version of Python
* latest version of Python.psutil
* latest version of Python.pythonnet
* latest version of Python.requests
* latest version of PySide6
* latest version of Pyinstaller

Steps:
* download the latest release
* download the commit from the branch that matches the version of the downloaded release
* replace the executable in the release by its corresponding .py files
* open cmd in the folder that contains the .py files
* input "pyinstaller.exe --onefile --icon=Bloodstained.ico Randomizer.py"
