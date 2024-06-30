from tkinter import ttk
from file_database import *
from logs_database import *
from helpers import *
from find_chrome_website import *
import shutil
import time

def findWebsite():
    # Start the Flask server from find_chrome_website
    server_thread = start_flask_server()
    # Wait for the server to start
    time.sleep(0.1)

    # Stop the Flask server
    stop_flask_server(server_thread)

    # Get the curURL after server has stopped
    url = get_current_url()
    print(url)
    #Only get the main website name
    components = url.split("/")
    for comp in components:
        if "." in comp: #The website name will have at least 1 "." from the domain name
            return comp


def move_downloaded_files_under_sorted_folder():
    # Get the most recent file in the indicated sorted folder path for later reference
    if getMostRecentFileInFolder(folderPath):
        mostRecentFile = getMostRecentFileInFolder(folderPath)
    else:
        mostRecentFile = -1

    while not stop_event.is_set(): # While the program is still running
        websiteName = findWebsite()
        if websiteName != False:
            if getMostRecentFileInFolder(folderPath):
                downloadedFile = getMostRecentFileInFolder(folderPath)

                if downloadedFile != mostRecentFile: # Makes sure the program only moves newly downloaded files
                    newFolderPath = os.path.join(folderPath, websiteName)

                    if not os.path.exists(newFolderPath):
                        os.makedirs(newFolderPath)
                    shutil.move(downloadedFile, newFolderPath)
                    updateLog(f"{downloadedFile} moved to {newFolderPath}", logText)

                #Update the most recent file
                mostRecentFile = getMostRecentFileInFolder(folderPath)

def update_detected_website_on_GUI():
    while True:
        websiteName = findWebsite()
        if websiteName:
            websiteLabel.config(text=f"Detected Website: {websiteName}") # Update the display detected website on GUI
        time.sleep(0.1) # Delay between HTTPS requests to ensure findWebsite() works correctly

def start_main_program():
    stop_event.clear()
    updateLog("Program Started", logText)
    curStatus.config(text="Status: Running") # Update status on GUI

    moveThread = threading.Thread(target=move_downloaded_files_under_sorted_folder)
    moveThread.daemon = True
    moveThread.start()

def stop_main_program():
    stop_event.set()
    updateLog("Program Stopped", logText)
    curStatus.config(text="Status: Stopped") # Update status on GUI

def main():
    global stop_event, folderPath
    global cur_path_to_tesseract, cur_sort_folder, curStatus, logText
    global websiteLabel, current_url

    try:
        stop_event = threading.Event()

        create_file_database()
        create_logs_database()

        folderPath = "placeholder"

        # Create GUI

        root = tk.Tk() # Shortcut
        root.title("Sort Downloads by Website of Origin by Andy Tong")
        root.geometry("500x270")

        # Create Tabs
        tabRoot = ttk.Notebook(root) # Shortcut

        mainTab = ttk.Frame(tabRoot) # Make the main tain
        tabRoot.add(mainTab, text='Main')
        logsTab = ttk.Frame(tabRoot) # Make the logs tab
        tabRoot.add(logsTab, text='Logs')

        tabRoot.pack(expand=1, fill='both')

        # Log tab layout (done first because some functions in the main tab rely on this)
        logText = tk.Text(logsTab, state=tk.DISABLED, wrap=tk.WORD)
        logText.pack(expand=1, fill='both')

        # Load logs when the logs tab is selected
        tabRoot.bind("<<NotebookTabChanged>>",
                     lambda event: loadLogs(logText) if tabRoot.index(tabRoot.select()) == 1 else None)

        cur_sort_folder = tk.Label(mainTab, text=f"Operating Folder: {folderPath}")
        cur_sort_folder.pack(pady=5)
        tk.Button(mainTab, text="Change Operating Folder", command=lambda:
            change_path_to_sort_folder(folderPath,store_sort_folder_file_path,updateLog,cur_sort_folder,logText)).pack(pady=5)

        # Access the stored file path that the user wants to move downloads from and store the folders with sorted files to
        # Prompt the user to input a valid one if none exists
        folderPath = verify_path_to_sort_folder(folderPath, get_stored_sort_folder_path, store_sort_folder_file_path,
                                                updateLog, cur_sort_folder)

        curStatus = tk.Label(mainTab, text="Status: Stopped")
        curStatus.pack(pady=20)

        # Always have a label that shows the detected website

        websiteLabel = tk.Label(mainTab, text="Detected Website: ")
        websiteLabel.pack(pady=0)

        update_website_thread = threading.Thread(target=update_detected_website_on_GUI)
        update_website_thread.daemon = True
        update_website_thread.start()

        # Frame for Start and Stop buttons to make them horizontal to each other
        buttonFrame = tk.Frame(mainTab)
        buttonFrame.pack(pady=20)

        tk.Button(buttonFrame, text="Start Sorting", command=lambda: start_main_program()).grid(row=0, column=0, padx=10)
        tk.Button(buttonFrame, text="Stop Sorting", command=lambda: stop_main_program()).grid(row=0, column=1, padx=10)

        # Cleanup old logs periodically
        cleanupInterval = 60 * 60 * 24  # Run cleanup once a day
        root.after(cleanupInterval, cleanup_old_logs)

        root.mainloop()

    except (KeyboardInterrupt, SystemExit):
        print("\n\nExiting program...")
        print("Program successfully exited")

if __name__ == "__main__":
    main()
