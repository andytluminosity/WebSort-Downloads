import ctypes
import pyautogui
import glob
import os
import pytesseract
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox

def findWebsite(pathToPytesseract):

    # Get the scale factor found in the Windows Settings display menu
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    # Take screenshot of website search bar using pyautogui according to the scaleFactor
    image = pyautogui.screenshot(region=(0, round(40 * scaleFactor), round(600 * scaleFactor), round(45 * scaleFactor)))

    pytesseract.pytesseract.tesseract_cmd = pathToPytesseract

    try:
        rawText = pytesseract.image_to_string(image)

        # Get the website url
        tempLst = rawText.split("/")
        for occ in tempLst:
            if "." in occ:
                tempLst = occ.split()  # Sometimes the raw text will include random spaces so this aims to get rid of everything non-URL
                for occ2 in tempLst:
                    if occ2.islower() and "." in occ2:  # everything in the inial URL must be in lower case and have at least one "."
                        return occ2
        return False
    except pytesseract.TesseractError:
        return False

def getMostRecentFileInFolder(folderPath):
    files = glob.glob(os.path.join(folderPath, '*')) #Refresh the list of files seen by the program
    if len(files)>0:
        return max(files, key=os.path.getctime)
    return False

def verify_path_to_tesseract(pathToPytesseract, get_stored_pytesseract_path, store_pytesseract_file_path, updateLog, cur_path_to_tesseract):
    # Access the stored pytesseract file path and prompt the user to input a valid one if none exists

    # Check if there is a stored pytesseract file path
    stored_path = get_stored_pytesseract_path()

    # Make sure that the stored path has tesseract.exe in it (program doesn't work if pytesseract modified)
    if stored_path and stored_path.find("tesseract.exe") >= 0:
        pathToPytesseract = stored_path
        cur_path_to_tesseract.config(
            text=f"Pytesseract Path: {pathToPytesseract}")  # Update the displayed path on GUI
        return pathToPytesseract
    else:
        # Prompt the user to input the file path

        input_path = r'{}'.format(
            askopenfilename(title="Select the File Path to Pytesseract\'s tesseract.exe"),
            mustexist=True, filetypes=[("Executable files", "*.exe")])

        if input_path and "tesseract.exe" in input_path:
            store_pytesseract_file_path(str(input_path))
            pathToPytesseract = input_path
            updateLog(f"Path to Pytesseract\'s tesseract.exe changed to {pathToPytesseract}")
            cur_path_to_tesseract.config(
                text=f"Pytesseract Path: {pathToPytesseract}")  # Update the displayed path on GUI
            return pathToPytesseract
        else:
            messagebox.showinfo("Error", "Please select the correct file path to Pytesseract\'s tesseract.exe")

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
            updateLog(f"Operating folder changed to {folderPath}")
            cur_sort_folder.config(text=f"Operating folder: {folderPath}")  # Update the displayed path on GUI
            return folderPath
        else:
            messagebox.showinfo("Error","Please select the a valid folder path to move downloads from "
                                "and store sorted folder in")

def change_path_to_tesseract(pathToPytesseract, store_pytesseract_file_path, updateLog, cur_path_to_tesseract):
    input_path = r'{}'.format(askopenfilename(title="Select the File Path to Pytesseract\'s tesseract.exe", filetypes=[("Executable files", "*.exe")]))
    if input_path and "tesseract.exe" in input_path:
        store_pytesseract_file_path(input_path)
        pathToPytesseract = input_path
        updateLog(f"Path to Pytesseract\'s tesseract.exe changed to {input_path}")
        cur_path_to_tesseract.config(text=f"Pytesseract Path: {pathToPytesseract}")
    else:
        messagebox.showinfo("Error","Please select the correct file path to Pytesseract\'s tesseract.exe")

    return pathToPytesseract

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
