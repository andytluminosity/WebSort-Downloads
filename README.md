# Sort Downloads by Website of Origin

A program that automatically new downloads into subfolders based on their source website located in the same downloads folder.

## Features

- Change the program's operating folder
- Start and stop the program at will
- Logs to keep track of changes made like when the program has been started, stopped, and moved a file (its old and new locations)
- A label that constantly displays the website you are on

## Installation

- [ ] Install Python3.9
	
  On Windows visit `https://www.python.org/downloads/windows/`
	- Click latest Python 3.9 release
	- Scroll down to the bottom to the section titled "Files"
	- Click the Windows Installer (64-bit) link to download the ".exe"
	- In File Explorer right click the file and click "Run as Administrator"
	- Check the boxes "Install launcher for all users (recommended)" and "Install Python 3.9 to path"
	
	On macOS 11+ (Intel) and macOS 11+ (Apple Sillicon) visit "`https://www.python.org/downloads/macos/`"
	- Click latest Python 3.9 release
	- Scroll down to the bottom to the section titled "Files"
	- Click the macOS 64-bit universal2 installer link to download the ".pkg"
	- Run the downloaded ".pkg"
	
    On Debian GNU/Linux 11+ based distros:
    - `sudo apt update`
    - `sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev`
    - `wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz`
    - `tar -xf Python-3.9.7.tgz`
    - `cd Python-3.9.7`
    - `./configure --enable-optimizations`
    - `make`
    - `sudo make altinstall`

   On Arch Linux based distros run:
	- `sudo pacman -S --needed base-devel git`
 	- `git clone https://aur.archlinux.org/python39.git`
  	- `cd python39`
  	- `makepkg -si`

- [ ]  Download and unzip or clone this repo
	- https://github.com/Raymo111/kahoot-answer-bot/archive/master.zip
	- `git clone https://github.com/Raymo111/kahoot-answer-bot.git`
