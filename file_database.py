import sqlite3

def create_file_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('file_paths.db')
    cursor = conn.cursor()

    # Create a table to store file paths if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paths (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL
        )
    ''')

    # Commit changes and close the connection

    conn.commit()
    conn.close()

def get_stored_pytesseract_path():
    # Connect to the SQLite database
    conn = sqlite3.connect('file_paths.db')
    cursor = conn.cursor()

    # Fetch the stored file path
    cursor.execute('SELECT file_path FROM paths WHERE id = 1')
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None

def get_stored_sort_folder_path():
    # Get the file path to where the program will store the folders
    # containing the new downloads corresponding to the website they were downloaded from

    # Connect to the SQLite database
    conn = sqlite3.connect('file_paths.db')
    cursor = conn.cursor()

    # Fetch the stored file path
    cursor.execute('SELECT file_path FROM paths WHERE id = 2')
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None

def store_pytesseract_file_path(file_path):
    conn = sqlite3.connect('file_paths.db')
    cursor = conn.cursor()

    # Check if there is already a stored path
    cursor.execute('SELECT * FROM paths WHERE id = 1')
    result = cursor.fetchone()

    if result:
        # Update the existing path
        cursor.execute('UPDATE paths SET file_path = ? WHERE id = 1', (file_path,))
    else:
        # Insert the new file path
        cursor.execute('INSERT INTO paths (id, file_path) VALUES (1, ?)', (file_path,))

    conn.commit()
    conn.close()

def store_sort_folder_file_path(file_path):
    conn = sqlite3.connect('file_paths.db')
    cursor = conn.cursor()

    # Check if there is already a stored path
    cursor.execute('SELECT * FROM paths WHERE id = 2')
    result = cursor.fetchone()

    if result:
        # Update the existing path
        cursor.execute('UPDATE paths SET file_path = ? WHERE id = 2', (file_path,))
    else:
        # Insert the new file path
        cursor.execute('INSERT INTO paths (id, file_path) VALUES (2, ?)', (file_path,))

    conn.commit()
    conn.close()