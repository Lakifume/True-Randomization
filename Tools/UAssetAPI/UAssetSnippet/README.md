# UAssetSnippet
This project is used to extend some of the UAssetAPI functionalities.

## Requirements
* dotnet 8

## Initial Setup
* Before anything, run `git submodule update --init` at the repo root

## VSCode Python Snippets
For better type hints in python using vscode, follow these steps:

* open a terminal in `SnippetSrc/`
  * run `dotnet restore`
  * run `dotnet tool restore`
  * run `dotnet build`
  * run `dotnet GeneratePythonNetStubs --dest-path="../typings" --target-dlls="./bin/Debug/netstandard2.0/UAssetSnippet.dll,./bin/Debug/netstandard2.0/UAssetAPI.dll"`
* install the Python and Pylance vscode extensions
* Pylance should be able to autocomplete UAssetAPI and UAssetSnippet types from now on

## Testing modifications
To makes changes to UAssetSnippet and test them, follow these steps:

* open a terminal in `SnippetSrc/`
  * run `dotnet restore`
  * run `dotnet build`
* copy the `UAssetSnippet.dll` from `./SnippetSrc/bin/Debug/netstandard2.0/` to the `./dist/Tools/UAssetAPI/` folder
* run the `Randomizer.exe`

Avoid making changes to the UAssetAPI project unless testing things out.
In which case, also drag the `UAssetAPI.dll` into the `/dist/Tools/UAssetAPI/` folder when building.

Never commit modified files in the UAssetAPI project