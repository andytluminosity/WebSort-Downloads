import glob
import os
from tkinter.filedialog import askdirectory
from tkinter import messagebox

def getMostRecentFileInFolder(folderPath):
    temp_extensions = (
    '.tmp', '.temp', '.bak', '.old', '~', '.~tmp', '.swp', '~$', '.crdownload', '.download', '.part', '.log', '.obj',
    '.pch', '.gch', '.ldb', '.tlog')

    files = glob.glob(os.path.join(folderPath, '*')) #Refresh the list of files seen by the program
    non_temp_files = [f for f in files if not f.endswith(temp_extensions)]
    if len(non_temp_files)>0:
        try: # Is necessary due to the SLIGHT time frame that a file is detected but already moved and no longer in folder
            return max(non_temp_files, key=os.path.getctime)
        except FileNotFoundError:
            return -1
    return -1

def verify_path_to_sort_folder(get_stored_sort_folder_path, store_sort_folder_file_path, cur_sort_folder):
    # Access the stored pytesseract file path and prompt the user to input a valid one if none exists

    # Check if there is a stored file path to a folder
    stored_path = get_stored_sort_folder_path()

    if stored_path:
        folderPath = stored_path
        cur_sort_folder.config(text=f"Operating Folder: {folderPath}")  # Update the displayed path on GUI
        return folderPath
    else:
        while True: # While a path has not been entered
            # Prompt the user to input the file path
            input_path = r'{}'.format(
                askdirectory(title="Select the Folder to Move Downloads From and Store Sorted Folders In"),
                mustexist=True)

            if input_path:
                store_sort_folder_file_path(str(input_path))
                folderPath = input_path
                cur_sort_folder.config(text=f"Operating Folder: {folderPath}")  # Update the displayed path on GUI
                return folderPath
            else:
                messagebox.showinfo("Error","Please select the valid folder path to move downloads from "
                                "and store sorted folder in")

def change_path_to_sort_folder(folderPath, store_sort_folder_file_path, updateLog, cur_sort_folder, logText):
    input_path = r'{}'.format(askdirectory(title="Select the Folder to Move Downloads From and Store Sorted Folders In"))
    if input_path:
        store_sort_folder_file_path(input_path)
        folderPath = input_path
        updateLog(f"Operating Folder changed to {input_path}",logText)
        cur_sort_folder.config(text=f"Operating Folder: {folderPath}")
    else:
        messagebox.showinfo("Error", "Please select a valid folder path to move downloads from and store sorted folder in")

    return folderPath
