# RetroRewindToolkit

Source code and build instructions for **Retro Rewind Toolkit v0.13 RC**, an offline save editor for **Retro Rewind - Video Store Simulator**.

The tool is designed to modify specific progression values stored in the game's local `.sav` files.

## Features

- Skip the tutorial.
- Change the player's money.
- Change the store level after level 1 has been reached naturally.
- Automatic backup creation before modifying a save.
- Automatic detection of Retro Rewind save files.
- Multi-language interface.
- No administrator privileges required.
- Works completely offline.

## Important usage notes

Retro Rewind must be **closed** before modifying a save.

Some values are not present in a newly created save until the game has initialized them:

- **Skip Tutorial:** available from a newly created save.
- **Money:** the player must purchase something and save the game at least once before the money value can be edited.
- **Store Level:** the save must reach **level 1 naturally** before the level can be edited.

The application creates a backup before modifying the original save.

## Source code

The complete Python source code used for this release is included in this repository:

`RetroRewindToolkit_v0.13_RC_FINAL.py`

The Python version can be run directly with **Python 3.8+**.

The graphical interface uses **Tkinter**.

## Building the Windows version

The Windows executable is built from the same Python source code available in this repository.

Install Python 3.8 or newer and PyInstaller:

```bash
pip install pyinstaller
```

From the directory containing the source file, build the application with:

```bash
pyinstaller --noconfirm --onedir --windowed --name RetroRewindToolkit RetroRewindToolkit_v0.13_RC_FINAL.py
```

PyInstaller will create the Windows build inside:

```text
dist/RetroRewindToolkit/
```

The resulting folder contains:

```text
RetroRewindToolkit.exe
_internal/
```

Both the executable and the `_internal` folder are required for the Windows version to run.

No installer is used.

## Security and transparency

Retro Rewind Toolkit only operates on local Retro Rewind save files selected or detected on the user's computer.

The source code is publicly available in this repository so that users and platform moderators can inspect the application's behavior and reproduce the Windows build.

The source `.py` file has also been checked with VirusTotal with no security vendors flagging it as malicious.

Because the Windows executable is packaged with PyInstaller and modifies binary game save files, some antivirus heuristic engines may classify the compiled executable as suspicious. The source code and build instructions are provided here for transparency and independent verification.

## Backups

Before a save is modified, Retro Rewind Toolkit creates an automatic backup.

Users should nevertheless keep their own backup of important save files before using any save editor.

## Disclaimer

Retro Rewind Toolkit is an unofficial community utility and is not affiliated with or endorsed by the developers or publishers of Retro Rewind - Video Store Simulator.
