# RetroRewindToolkit

Source code and build instructions for **Retro Rewind Toolkit v0.13**, an offline save editor for **Retro Rewind - Video Store Simulator**.

The current Windows release is developed in **C# using .NET 8 and Windows Forms**.

The tool is designed to modify specific progression values stored in the game's local `.sav` files.

## Features

- Skip the tutorial.
- Change the player's money.
- Change the store level after level 1 has been reached naturally.
- Automatic backup creation before modifying a save.
- Automatic detection of Retro Rewind save files.
- Multi-language interface:
  - English
  - Español
  - Français
  - Deutsch
  - Italiano
  - Português
- No administrator privileges required.
- Works completely offline.

## Important usage notes

Retro Rewind must be **closed** before modifying a save.

Some values are not present in a newly created save until the game has initialized them:

- **Skip Tutorial:** available from a newly created save.
- **Money:** the player must purchase something and save the game at least once before the money value can be edited.
- **Store Level:** the save must reach **level 1 naturally** before the level can be edited.

The application creates an automatic backup before modifying the original save.

## Current Windows source code

The source code for the current Windows release is included in this repository.

Main files:

- `Program.cs` — application entry point.
- `MainForm.cs` — Windows Forms user interface.
- `SaveOps.cs` — save detection, reading, validation, backup and modification operations.
- `Translations.cs` — interface translations.
- `RetroRewindToolkit.csproj` — .NET 8 project and Windows build configuration.
- `RetroRewindToolkit.ico` — application icon.
- `BUILD_FINAL_SINGLE_FILE_WINDOWS.bat` — reproducible Windows build script.

The application targets:

- **C# / .NET 8**
- **Windows Forms**
- **Windows x64**
- **Single-file publication**
- **Framework-dependent deployment**

## Building the current Windows version

### Requirements

Install the **.NET 8 SDK**.

From the repository directory, run:

`BUILD_FINAL_SINGLE_FILE_WINDOWS.bat`

Or build manually with:

`dotnet publish RetroRewindToolkit.csproj -c Release -r win-x64 --self-contained false -p:PublishSingleFile=true -p:DebugType=None -p:DebugSymbols=false -o Release`

The final application is generated as:

`Release/RetroRewindToolkit.exe`

No installer is required.

Because this is a framework-dependent build, the target computer requires the **.NET 8 Desktop Runtime**.

## Security and transparency

Retro Rewind Toolkit works entirely offline.

It does not connect to the Internet and does not require administrator privileges.

The application only operates on local Retro Rewind save files and creates a backup before writing changes.

The complete source code for the current Windows release is publicly available in this repository so that users and platform moderators can inspect the application's behavior and reproduce the Windows build independently.

The current Windows executable was built directly with the official .NET SDK using the build process documented above.

### VirusTotal

The current Windows executable has been analyzed by VirusTotal with **0 security vendors flagging the file as malicious**.

SHA-256:

`6617e4255b3e96126b1284758231e9558286e58e816d706af8421178406c1d58`

VirusTotal report:

https://www.virustotal.com/gui/file/6617e4255b3e96126b1284758231e9558286e58e816d706af8421178406c1d58/detection

## Previous Python implementation

The repository also contains:

`RetroRewindToolkit_v0.13_RC_FINAL.py`

This is the **previous Python implementation** of Retro Rewind Toolkit and is retained for historical reference and transparency.

It is **not the source used to build the current C#/.NET Windows executable**.

The current Windows release should be built from the `.cs` source files and `RetroRewindToolkit.csproj` using the .NET 8 build instructions above.

## Backups

Before a save is modified, Retro Rewind Toolkit creates an automatic backup.

Users should nevertheless keep their own backup of important save files before using any save editor.

## Disclaimer

Retro Rewind Toolkit is an unofficial community utility and is not affiliated with or endorsed by the developers or publishers of Retro Rewind - Video Store Simulator.
