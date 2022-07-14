# True-Randomization

New and improved randomization options for Bloodstained randomizer. Negates about everything that the game's built-in randomizer mode does to apply all of the necessary logic and new features.

![Screenshot (337)](https://user-images.githubusercontent.com/56451477/178378598-0cedda11-581d-4a6d-8b33-c9d9e5b0ae52.png)

## How to build from source

Requirements:
* latest version of Python
* latest version of PySide6
* latest version of Pyinstaller

Steps:
* open cmd in the folder that contains the .py files
* input "pyinstaller.exe --onefile --icon=Bloodstained.ico Randomizer.py"

## FAQ

Why is picking seed 17791 required ?
* since the game randomizer provides no option to not shuffle the item containers the only way for a mod to apply its custom logic is by mapping out a specific seed to then adapt item placement based on that

Well then why not build this mod over story mode ?
* story mode presents several issues that are not present in the randomizer mode such as events that can softlock and containers being unable to change visually

Why does Craftwork always have the Craftwork shard and Glutton Train the hammer knuckle shard ?
* these two actually turn out to be a real pain in the ass, giving them a different shard will softlock you in their room upon defeating them

Why do various other things seem to play a bit differently than in the vanilla game ?
* to improve the randomizer experience or even the game experience in general this mod fixes multiple aspects of the game's difficulty balance to make it less reliant on specific strategies and exploits, sorry void ray enthousiasts

What do the special modes even have to do with randomizer ?
* absolutely nothing, they're just there to provide other non-randomized gameplay options for those who would want to mix things up a bit
