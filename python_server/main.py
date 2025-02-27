from tkinter import ttk
from file_database import *
from logs_database import *
from special_cases_tab import *
from helpers import *
from find_chrome_website import *
import shutil
import time

def updateVariables():
    def findWebsite():
        global cur_website_name
        while True:
            # Start the Flask server from find_chrome_website
            server_thread = start_flask_server()
            # Wait for the server to start
            time.sleep(0.1)

            # Stop the Flask server
            stop_flask_server(server_thread)

            # Get the curURL after server has stopped
            url = get_current_url()
            print(url)
            # Only get the main website name
            components = url.split("/")
            for comp in components:
                if "." in comp:  # The website name will have at least 1 "." from the domain name
                    if len(comp) >= 5:  # Ensure that the starting "www." is removed
                        if 'www.' in comp:
                            cur_website_name = comp[4:]
                            break
                    cur_website_name = comp
                    break

    findWebsite()

def move_downloaded_files_under_sorted_folder():
    global cur_website_name
    global folderPath
    global created_folder_paths
    # Get the time the most recent file in the indicated sorted folder path was created for later reference
    try:
        mostRecentFileTime = os.path.getctime(getMostRecentFileInFolder(folderPath))
    except (OSError,FileNotFoundError) as e:
        mostRecentFileTime = -1

    while not stop_event.is_set(): # While the program is still running
        if getMostRecentFileInFolder(folderPath):  # If there is a file in the operating folder
            downloadedFile = getMostRecentFileInFolder(folderPath)

            if downloadedFile == -1:
                continue

            # Makes sure the program only moves newly downloaded files
            if downloadedFile not in created_folder_paths and os.path.getctime(downloadedFile) > mostRecentFileTime:
                if cur_website_name != False:

                    # If a special case has been made, move it to the specified folder path
                    # Second condition accounts for if www. was put into a special case

                    if check_existence_of_websiteName(cur_website_name) or check_existence_of_websiteName("www." + cur_website_name):
                        newFolderPath = get_folder_path(cur_website_name)

                    # Otherwise, move it to a folder titled websiteName
                    else:
                        newFolderPath = os.path.join(folderPath, cur_website_name)

                    print("New Folder Path:", newFolderPath)
                    if not os.path.exists(newFolderPath):
                        os.makedirs(newFolderPath)
                        # Ensure the program doesn't try to move the newly created folder into said folder
                        created_folder_paths.append(newFolderPath)

                    try:
                        shutil.move(downloadedFile, newFolderPath)
                        updateLog(f"{downloadedFile} moved to {newFolderPath}", logText)
                    except shutil.Error:
                        print(f"\n\nCRITICAL ERROR: {downloadedFile} already exists in {newFolderPath}\n\n")

def update_detected_website_on_GUI():
    global cur_website_name
    while True:
        print('Current Website:', cur_website_name)
        if cur_website_name:
            websiteLabel.config(text=f"Detected Website: {cur_website_name}") # Update the display detected website on GUI
        time.sleep(0.1) # Delay between HTTPS requests to ensure findWebsite() works correctly

def update_sort_folder_path():
    global folderPath
    folderPath = change_path_to_sort_folder(folderPath, store_sort_folder_file_path, updateLog, cur_sort_folder, logText)

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
    global stop_event, folderPath, cur_website_name, created_folder_paths
    global cur_path_to_tesseract, cur_sort_folder, curStatus, logText
    global websiteLabel, current_url

    try:
        stop_event = threading.Event()

        create_file_database()
        create_logs_database()
        create_special_case_database()

        folderPath = "N/A"
        cur_website_name = False
        created_folder_paths = []

        # Create GUI

        root = tk.Tk() # Shortcut
        root.title("WebSort Downloads")
        root.geometry("500x270")

        # Create Tabs
        tabRoot = ttk.Notebook(root) # Shortcut

        mainTab = ttk.Frame(tabRoot) # Make the main tain
        tabRoot.add(mainTab, text='Main')
        logsTab = ttk.Frame(tabRoot) # Make the logs tab
        tabRoot.add(logsTab, text='Logs')
        special_cases_tab = ttk.Frame(tabRoot) # Make the
        tabRoot.add(special_cases_tab, text='Special Cases')

        tabRoot.pack(expand=1, fill='both')

        # Log tab layout (done first because some functions in the main tab rely on this)
        logText = tk.Text(logsTab, state=tk.DISABLED, wrap=tk.WORD)
        logText.pack(expand=1, fill='both')

        # Load logs when the logs tab is selected
        tabRoot.bind("<<NotebookTabChanged>>",
                     lambda event: loadLogs(logText) if tabRoot.index(tabRoot.select()) == 1 else None)

        cur_sort_folder = tk.Label(mainTab, text=f"Operating Folder: {folderPath}")
        cur_sort_folder.pack(pady=5)
        tk.Button(mainTab, text="Change Operating Folder", command=update_sort_folder_path).pack(pady=5)

        # Access the stored file path that the user wants to move downloads from and store the folders with sorted files to
        # Prompt the user to input a valid one if none exists
        folderPath = verify_path_to_sort_folder(get_stored_sort_folder_path, store_sort_folder_file_path, cur_sort_folder)

        curStatus = tk.Label(mainTab, text="Status: Stopped")
        curStatus.pack(pady=20)

        # Constantly update the current website name and sort/operating folder path
        update_variables_thread = threading.Thread(target=updateVariables)
        update_variables_thread.daemon = True
        update_variables_thread.start()

        # Always have a label that shows the detected website
        websiteLabel = tk.Label(mainTab, text="Detected Website: ")
        websiteLabel.pack(pady=0)

        update_website_display_thread = threading.Thread(target=update_detected_website_on_GUI)
        update_website_display_thread.daemon = True
        update_website_display_thread.start()

        # Frame for Start and Stop buttons to make them horizontal to each other
        buttonFrame = tk.Frame(mainTab)
        buttonFrame.pack(pady=20)

        tk.Button(buttonFrame, text="Start Sorting", command=lambda: start_main_program()).grid(row=0, column=0, padx=10)
        tk.Button(buttonFrame, text="Stop Sorting", command=lambda: stop_main_program()).grid(row=0, column=1, padx=10)

        # Cleanup old logs periodically
        cleanupInterval = 60 * 60 * 24  # Run cleanup once a day
        root.after(cleanupInterval, cleanup_old_logs)

        # Database Tab

        labels = []
        #tk.Label(special_cases_tab, text="Website Name:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Button(special_cases_tab, text="Add Special Case", command= lambda: open_add_special_case_window(logText, labels, special_cases_tab)).grid\
            (row=0, column=1, columnspan=5, padx=10, pady=10, sticky='ew')

        # Add an empty column at the beginning to shift everything to the right (to centre align)
        special_cases_tab.grid_columnconfigure(0, minsize=50)

        # Put in the initial data
        refresh_special_cases_gui(labels, special_cases_tab, logText)

        root.mainloop()

    except (KeyboardInterrupt, SystemExit):
        print("\n\nExiting program...")
        print("Program successfully exited")

if __name__ == "__main__":
    main()
