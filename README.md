# WebSort Downloads

### Note: Only works for Google Chrome

A program that, by default, automatically sorts new downloads into subfolders based on their source website located in the same downloads folder. You can control where downloads from certain websites are sorted to with `Special Cases`. The source website is detected using Chrome API.

## Features

- Change the program's operating folder
- Start and stop the program at will
- Logs to keep track of changes made like when the program has been started, stopped, and moved a file (its old and new locations)
	- Note: Any logs older than 2 weeks will automatically be deleted to save memory
- A label that constantly displays the website you are on
- Customizable special cases that allow control over where downloads from certain websites go

## Installation

- [ ] Install Python 3.9
	
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
    - `wget https://www.python.org/ftp/python/3.9.12/Python-3.9.12.tgz`
    - `tar -xf Python-3.9.12.tgz`
    - `cd Python-3.9.12`
    - `./configure --enable-optimizations`
    - `make`
    - `sudo make altinstall`

   On Arch Linux based distros run:
	- `sudo pacman -S --needed base-devel git`
 	- `git clone https://aur.archlinux.org/python39.git`
  	- `cd python39`
  	- `makepkg -si`
  	  
On other Linux based distros install python3.9 from your package manager.

- [ ]  Download the main zip file from the latest release notes
	- [Latest release notes](https://github.com/andytluminosity/WebSort-Downloads/releases/tag/v1.0)
 
- [ ] Install Dependencies
	- `python3.9 -m pip install flask flask_cors` / `python -m pip install flask flask_cors` / `py -m pip install flask flask_cors`
   
## Usage

- [ ] Add Chrome extension to Chrome
	- Go to the Extensions page by entering chrome://extensions in a new tab. (By design chrome:// URLs are not linkable.)
	  Alternatively, click the Extensions menu puzzle button and select Manage Extensions at the bottom of the menu.
	  Or, click the Chrome menu, hover over More Tools, then select Extensions.
	- Enable Developer Mode by clicking the toggle switch next to Developer mode.
	- Click the Load unpacked button and select the `url_sender_extension` folder	
	- Ensure that the extension is turned on
 - [ ] Start the program
	- Simple open the start.exe application within the `python_frontend` folder (it simply is a shortcut to running main.py)
 	- It is recommended to have this application pinned to your taskbar
 	- Your antivirus will likely flag this application as dangerous so creating an exception is necessary. See **File Safety** if you are concerned about the well-being of your files
 - [ ] Select the operating folder path
	- Select the folder path that your downloads are automatically saved to (typically `C:\Users\YOUR_USER_NAME\Downloads`)
 	- The program will save this folder path so you will only have to input it once
 	- You may change the operating folder path at any time
 - [ ] Create special cases (optional)
	- Special cases are cases where users can choose the folder all files downloaded from a certain website are automatically sent to
	- Add a special case
		- Click the 'Add Special Case' button in the `Special Cases` tab
  		- Enter the website's name and the folder path all downloads from that website will be redirected to
			- Note: The website's name should only include the main URL without anything after the slashes
    		- Eg. Valid: `google.com` Invalid: `google.com/maps`. Alternatively, enter whatever is shown in the `Detected Website` label in the `Main` tab when on the desired website
      		- Finally, click the 'Add' button. The special case will then appear in the `Special Cases` tab
   - Delete a special case
      - In the `Special Cases` tab, simply click the `X` next to the special case you want to delete
      - Confirm the deletion when prompted

## File Safety
- The program can only move files with absolutely **no ability to delete them**. You may check the old and new location of moved files in the `Logs` tab

## Known Issues / Troubleshooting

- [ ] Download is being sorted into the wrong folder / Current website is not being correctly detected
	- There is a slight delay when detecting the current website you are on when accessing Chrome API. It is recommended to wait for around 1 or 2 seconds to download a file after visiting a new website.
 	You can always check which website is being detected using the `Detected Website:` label on the GUI
- [ ] Only some downloads are being sorted into the desired folder (>v1.1.1)
	- The time it takes for certain downloads to be sorted into folders is directly proportional to its size. As a rule of thumb, it is recommended to wait 0.5-1 second before downloading another file
- [ ] Current website is not being detected at all
	- First reload/refresh the Chrome extension in developer mode. If the problem persists, remove and re-add the Chrome extension (see **Usage** for instructions on enabling developer mode and re-adding the extension)

## Reporting Other Issues
- When reporting other issues, please run the program using start_debug.exe, recreate the issue, and copy-paste everything that is said on the console into a .txt file. It makes fixing the issue a lot easier!

## Contributors
- [andytluminosity](https://github.com/andytluminosity) - Main Programming
- [Raymo111](https://github.com/Raymo111/kahoot-answer-bot) - Instructions to install Python 3.9
