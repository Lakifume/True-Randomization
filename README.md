# True Randomization

The randomizer that aims to accomplish what vanilla rando doesn't.

# Requirements

- Windows 10 and above

# Setup

Run the executable and start by specifying the path to where your Bloodstained game is installed. From there simply pick your options and press Generate.
If you are unusure what an option does hover over its widget to see a tooltip.
If randomization options were selected this will prompt you to choosing a seed for this rando to use, here you can input text and/or numbers.
The Test Seed button is there to give a quick preview of what the key item placement will be like, useful if you're looking for a specific setup.
Lastly press Confirm and wait through the progress bar. The first time you do this will take longer since the assets will need to be initially imported and cached.
The mod will be automatically placed in the right folder so all you need to do from there is boot up the game and begin a new story mode file.

If you get stuck and need to look at the solution open up the map editor and go to Tools > Key Locations.
If the seed turns out to be unbeatable report it on NexusMods, Github or Discord and specify the seed number, the map and the difficulty.

# In-game hotkeys

F1: Toggle CC effect notifications (Crowd Control only)
F2: Force Craftwork/Glutton Train/IGA boss fights to end if the doors fail to open after getting their shard
F3: Instantly warp to the starting room of the game
F4: While on the title screen toggle automatic starting DLC items (disabled by default)

# Things to know when using this rando

- The only options that affect the seeding of key placements are the map, the difficulty and whether random enemies is on or not.
- The "beatable" field present in the spoiler can only be false if the custom map isn't built properly or if said map is incompatible when playing as Bloodless
- The few item checks that are normally upgrades offscreen can become chests that need pressing up to be opened.
- Three new checks were added to the game: one shard candle in Celeste's Room, one shard candle in m11UGD_019 and a shard drop to the Journey boss.
- The Dullahammer EX and Giant Dullahammer Head enemies share the same shard drop as their regular counterparts.
- There is a slight edge case where getting an enemy to drop a key shard but exiting the room before getting it will prevent it from dropping ever again, reload and try again if this happens.

# Things to know when playing on custom maps

- Always have waystones in your inventory to prevent softlocks, they're cheap and guaranteed at the shop.
- Riding the train must be done before the destination room event is triggered, otherwise you could be permanently locked out of the train.
- Enemies are overall rebalanced to scale with the new area order though since some of them are found throughout the castle you may encounter a few strong enemies early on.
- For a map to be beatable in Bloodless mode it needs to not lock any pre-portal bosses behind the Den portal and to have Gremory accessible before the Dimension Shift room.

# Things to know about Classic 2 rando

- Only checks that originally have real items are shuffled, candles and walls that drop mana or cake are unchanged.
- Boss drops are replaced with chests in the middle of the arena to be able to carry any item type.
- You can no longer drop through the sand in Meggido to reach Lethe Cavern without turning it into water first with True Sight.
- You can now adjust the intensity level of this mode with the difficulty toggles on the interface ("Hard" being equivalent to vanilla).

# Updates

The devs have already stated that there will be no more updates to Bloodstained's built in randomizer mode despite being flawed and incomplete.
This mod however will always be wide open for suggestions and receive updates based on the game's outcome.

# Glitches

Here are some known game glitches to watch out for:

- Occasionally some room ambient sounds will fail to stop playing when transitioning to the next room and linger forever. Exit to title screen and load the file again to fix it.
- Dashing into the narrow hole in m17RVA_003 with accelerator has a chance to clip you into the ceiling and softlock, try to slow down when you get there.
- Sliding into a warp gate as Zangetsu or Bloodless can clip you into the ceiling if the exit is positioned upside down, try to walk into them to avoid this.

# Troubleshooting

- If the program fails to open when double clicking the exe open it via command prompt instead to be able to read the error.
- If you get an error get the zip file again, right click on it, go to Properties, check Unblock and extract again.
- If the program gets stuck while a process is loading check the command window behind the interface to see if any error messages show up.
- If problems still persist open an issue on Github or on Discord and try to be as specific as possible.

# Changelog

3.0.5:
- Fixed an issue where OD could clip into the ground on custom maps
- 

3.0.4:
- Fixed Bloodless not spawning properly when her room is moved
- Fixed an issue with duplicating item descriptions
- Fixed an issue where swords could no longer break candles

3.0.3:
- Added randomization support for Classic Mode 2
- Made Bloodless mode available in-game without needing a cheatcode
- Added 8 Bit Nightmare to the music randomization

3.0.2:
- Drastically improved the speed of asset importing
- Fixed an issue where DLC could not be detected from other drives
- Added proper error logging to the map editor

3.0.1:
- Updated the randomizer to the latest patch of the game
- Made it so that starting DLC items can be toggled in-game
- Included costume items in the random item pool based on the user's owned DLC
- Added an option to ignore all DLC during the seed generation

3.0.0:
- Added Accelerator in logic
- Fixed the Crafwork, Glutton Train and IGA softlocks and randomized their shards
- Added the option to customize which outfit colors can be randomly chosen
- Added an optional feature for randomly selecting mods to apply to the game
- Moved the browse map button next to random room layout and allow saving selection to config
- Moved random background music from a cheatcode to a checkbox
- Improved background music rando accuracy
- Improved room focus visibility in the map editor
- Added the option to move the map editor view with the middle mouse button
- Fixed some window sizing issues

2.9.3:
- Fixed an issue where snapping several rooms at once could shift their position in the map editor
- Added a tool for map completion check in the map editor
- Prevented use of Dimension Shift to bypass the Craftwork staircase in m07LIB_023
- Logic improvements

2.9.2:
- Added black and white variants to the random outfit color selection
- Added a Galleon transition room by default when starting the map editor
- Added mouse wheel shortcuts to zoom in the map editor
- Added right click menu for quick room actions in the map editor

2.9.1:
- Split random levels and tolerances options between regular enemies and bosses
- Added options to customize the weighting of certain randomization settings
- Added simplified parameter string field to facilitate the sharing of randomization settings
- Added a discord server link to the interface

2.9.0:
- Rebuilt progression logic to automatically adapt to any custom map layout
- Removed logic editing tools from the map editor
- Added a spoiler log flag to notify if a map is beatable or not
- Made it so that the tower elevator has activation levers on either side when playing on custom maps
- Fixed an issue where rare occurences of enemy rando seeds would fail to generate

2.8.4:
- Fixed an issue where non-DLC owners could not generate the pak file

2.8.3:
- Added Craftwork shard in logic and created a temporary workaround against the boss softlock until a better solution is found

2.8.2:
- Fixed enemy rando not working in the Kingdom 2 Crowns area
- Fixed an issue where the map editor could no longer read spoiler logs
- Fixed an issue where opening certain area doors could cause softlocks

2.8.1:
- Fixed an occasional game crash with enemy rando
- Changed starting items to a user-input text field

2.8.0:
- Fixed an issue where some upgrades could not be collected
- Fixed an issue where blue chests could have duplicate materials
- Other minor fixes

2.7.9:
- Added the option to randomize enemy locations
- Logic improvements

2.7.8:
- Fixed an issue where long imported musics didn't loop properly
- Fixed an issue where backer portraits would shuffle with duplicates
- Improved shard damage calculation
- Fixed an auto update issue where the previous program failed to close automatically
- Added the possibility to view the game's map display limits by pressing space bar in the map editor
- Added 4 new items into the game

2.7.7:
- Added interactable doors in the entrance spike tunnels to prevent tanking through
- Fixed new shard candles missing their top mesh piece
- Moved the new Aqua Stream shard candle to m11UGD_019
- Logic improvements

2.7.6:
- Implemented the ability to add new music slots into the game
- Made it so that overworld pool rando also affects drops in Classic Mode
- Added dialogue rando support for japanese voices
- Fixed an issue with key chests dropping nothing in m20JRN_002

2.7.5:
- Fixed an issue where key items could not end up in m20JRN_002
- Fixed an oversight that prevented Mystical Scarf from being in the shop
- Fixed some enemy resistances not scaling properly with levels
- Added more guaranteed shop items such as bit coins and seeds

2.7.4:
- Implemented the Journey crossover content in the randomizer
- Created a workaround for the Bathin boss softlock when entered from the left
- Made it so that the Zangetsuto portal gate always gets connected to its previous requirements
- Fixed a vanilla oversight where opening a lever door in cathedral also opened one in hall
- Fixed an auto updater issue when trying to extract the downloaded zip

2.7.3:
- Added the ability to duplicate save/warp/transition rooms in the map editor
- Added a shard candle in underground containing Aqua Stream by default
- Added a shard candle in Celeste's Room containing Familiar: Igniculus by default
- Made it so that backer door positions also update like other doors
- Made it so that connecting a backer room to another area automatically updates its properties
- Other minor improvements

2.7.2:
- Added full support for usage of this mod with story mode and dropped support for randomizer mode
- Made it so that item containers update based on their content
- Made it so that some room objects such as doors update based on its adjacent rooms
- Added new warping gates to give extra characters access to every corner of the castle
- Slightly simplified map logic by automatically flagging rooms with self contained obstacles
- Reworked dialogue rando to fix every known issue
- Reduced the amount of random blue chests
- Deleted vanilla rando from the game

2.7.1:
- Implemented direct usage of UAssetAPI to optimize process
- Made it so that game assets are extracted from the user's installation directly
- Other improvements

# How to add random mod selection via the randomizer

If you want this program to apply extra pak mods at random you can do so by placing them by groups under Data\Mod\[yourmodgroup]\[pakfiles]

# How to add your own musics into the game via the randomizer

Eternity Audio Tool: https://mega.nz/file/W5NHxDYD#IM7xirUu1-K8e34lINmgC3MFqG1OWFTuscbSptK5fRw

- Get a WAV of the music you want to add. If you want your music to have a custom loop you will need to add loop points into your WAV, you can accomplish this with tools such as Wavosaur.
- Open Eternity Audio Tool, go to File > Convert Files to HCA, select your WAV and use the loop data option. This will output an HCA file in the same folder.
- Grab the HCA, put it in the True Randomization\Data\Music folder and rename it using the following naming convention: ACT{2 digits number}_{3 character acronym}
- Go to MapEdit\Data\Translation, open MusicTranslation.json and add an entry with the music id as the key (BGM_m{your 2 digits number}{your 3 character acronym}) and its readable name as the value.
- Assign this new track to any room of your choice.