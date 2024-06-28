import glob
import os
from tkinter.filedialog import askdirectory
from tkinter import messagebox

def getMostRecentFileInFolder(folderPath):
    files = glob.glob(os.path.join(folderPath, '*')) #Refresh the list of files seen by the program
    if len(files)>0:
        return max(files, key=os.path.getctime)
    return False

def verify_path_to_sort_folder(folderPath, get_stored_sort_folder_path, store_sort_folder_file_path,updateLog, cur_sort_folder):
    # Access the stored pytesseract file path and prompt the user to input a valid one if none exists

    # Check if there is a stored file path to a folder
    stored_path = get_stored_sort_folder_path()

    if stored_path:
        folderPath = stored_path
        cur_sort_folder.config(text=f"Operating folder: {folderPath}")  # Update the displayed path on GUI
        return folderPath
    else:
        # Prompt the user to input the file path
        input_path = r'{}'.format(
            askdirectory(title="Select the Folder to Move Downloads From and Store Sorted Folders In"),
            mustexist=True)

        if input_path:
            store_sort_folder_file_path(str(input_path))
            folderPath = input_path
            cur_sort_folder.config(text=f"Operating folder: {folderPath}")  # Update the displayed path on GUI
            return folderPath
        else:
            messagebox.showinfo("Error","Please select the a valid folder path to move downloads from "
                                "and store sorted folder in")

def change_path_to_sort_folder(folderPath, store_sort_folder_file_path, updateLog, cur_sort_folder):
    input_path = r'{}'.format(askdirectory(title="Select the Folder to Move Downloads From and Store Sorted Folders In"))
    if input_path:
        store_sort_folder_file_path(input_path)
        folderPath = input_path
        updateLog(f"Operating folder changed to {input_path}")
        cur_sort_folder.config(text=f"Operating folder: {folderPath}")
    else:
        messagebox.showinfo("Error", "Please select a valid folder path to move downloads from and store sorted folder in")

    return folderPath