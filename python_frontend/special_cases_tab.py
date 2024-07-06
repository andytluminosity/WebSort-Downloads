from special_cases_database import *
from main import *
import tkinter as tk
from tkinter.filedialog import askdirectory
from logs_database import *

def delete_special_case(row, labels, dbTab, logText):
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()

    # Fetch the websiteName and id of the specific row
    c.execute("SELECT websiteName FROM websites ORDER BY websiteName ASC LIMIT 1 "
              "OFFSET ?", (row-1,))
    websiteName = c.fetchone()[0]
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{websiteName}'?"):
        delete_from_database(websiteName)
        updateLog(f"Deleted Special Case: {websiteName}", logText)
        refresh_special_cases_gui(labels, dbTab, logText)

def open_add_special_case_window(logText, labels, dbTab):
    folderPath = ""
    def add_website(logText):
        nonlocal folderPath
        if folderPath:
            websiteName = website_entry.get()
            if not check_existence_of_websiteName(websiteName): #Store the special case if one doesn't already exist for the website
                store_special_case(websiteName, folderPath)
                updateLog(f"Added Special Case: All files from \"{websiteName}\" will be moved to {folderPath}",
                          logText)

            else: # Otherwise ask the user if they want to replace it
                existing_folder_path = get_folder_path(websiteName)
                if messagebox.askyesno("Duplicate Special Case", f"A special case already exists"
                                                                 f"where all downloads from {websiteName} are redirected to {existing_folder_path}. Would you like to replace it?"):
                    delete_from_database(websiteName)
                    store_special_case(websiteName, folderPath)
                    updateLog(f"Added Special Case: All files from \"{websiteName}\" will be moved to {folderPath}",
                              logText)

            refresh_special_cases_gui(labels, dbTab, logText)

            # Close the window
            add_window.destroy()
        else:
            messagebox.showinfo("Error", "Please select a folder path")
            # Ensure that the add_window is in front of the initial main window after the popup
            add_window.focus_force()

    def select_folder_path():
        nonlocal folderPath
        folderPath = r'{}'.format(
            askdirectory(title="Select the Folder to Move Downloads From and Store Sorted Folders In"),
            mustexist=True)
        # Update the folder path entry field
        curFolderPath.config(text=f"Folder Path: {folderPath}")
        #Ensure that the add_window is in front of the initial main window after selecting the folder path
        add_window.focus_force()

    add_window = tk.Toplevel()
    add_window.title("Add Website")
    add_window.geometry('350x200')

    # Add empty column to centre align everything (move everything to the right)
    add_window.grid_columnconfigure(0, minsize=50)

    tk.Label(add_window, text="Website Name:").grid(row=0, column=1, padx=10, pady=10)
    website_entry = tk.Entry(add_window)
    website_entry.grid(row=0, column=2, padx=10, pady=10)

    curFolderPath = tk.Label(add_window, text="Folder Path:")
    curFolderPath.grid(row=1, column=1, columnspan=2,padx=10, pady=10,sticky='ew')
    folder_path_entry = tk.Button(add_window,text="Select Folder Path",command=select_folder_path)
    folder_path_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

    tk.Button(add_window, text="Add", command=lambda: add_website(logText)).grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    dbTab.wait_window(add_window)

def refresh_special_cases_gui(labels, special_cases_tab, logText):
    # Fetch the logs from the database
    conn = sqlite3.connect('websites.db')
    cursor = conn.cursor()
    cursor.execute('SELECT websiteName, folderPath FROM websites ORDER BY websiteName ASC')
    logs = cursor.fetchall()
    conn.close()

    #Delete all existing labels
    for label in labels:
        label.grid_forget()  # Remove the label from the grid
        label.destroy()  # Destroy the label widget
    labels.clear()  # Clear the list of labels

    #Add an empty column to leave space between entries and delete button
    special_cases_tab.grid_columnconfigure(4, minsize=50)
    special_cases_tab.grid_columnconfigure(2, minsize=50)

    # Insert the logs into the text widget. Website, folder path, and delete buttons in cols 1,2, and 3 respectfully
    for row, (websiteName,folderPath) in enumerate(logs):
        new_website_label = tk.Label(special_cases_tab, text=f"{websiteName}", anchor='w')
        new_website_label.grid(row=row+2, column=1, pady=5,sticky='w')

        new_folder_label = tk.Label(special_cases_tab, text=f"{folderPath}", anchor='w')
        new_folder_label.grid(row=row+2, column=3, pady=5,sticky='w')

        delete_button = tk.Button(special_cases_tab, text="X", command=lambda row=row + 1: delete_special_case(row, labels, special_cases_tab, logText))
        delete_button.grid(row=row+2, column=5, pady=5,sticky='ew')

        labels.append(new_website_label)
        labels.append(new_folder_label)
        labels.append(delete_button)