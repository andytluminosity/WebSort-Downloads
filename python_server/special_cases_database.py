import sqlite3

def create_special_case_database():
    conn = sqlite3.connect('special_cases.db')
    c = conn.cursor()

    #Create a table to store special cases if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS websites (id INTEGER PRIMARY KEY, 
        websiteName TEXT NOT NULL, folderPath TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def check_existence_of_websiteName(checkWebsite):
    conn = sqlite3.connect('special_cases.db')
    c = conn.cursor()

    query = "SELECT EXISTS(SELECT 1 FROM websites WHERE websiteName = ? LIMIT 1)"
    c.execute(query,(checkWebsite,))
    exists = c.fetchone()[0]
    conn.close()
    return exists

def get_folder_path(websiteName):
    conn = sqlite3.connect('special_cases.db')
    cursor = conn.cursor()

    cursor.execute("SELECT folderPath FROM websites WHERE websiteName = ?", (websiteName,))
    # Fetch the result
    result = cursor.fetchone()

    conn.close()

    # Return the result
    if result:
        return result[0]
    else:
        return None

def store_special_case(websiteName, folderPath):
    conn = sqlite3.connect('special_cases.db')
    c = conn.cursor()
    c.execute("INSERT INTO websites (websiteName, folderPath) VALUES (?, ?)",
              (websiteName, folderPath))
    conn.commit()
    conn.close()

def delete_from_database(websiteName):
    if check_existence_of_websiteName(websiteName):
        conn = sqlite3.connect('special_cases.db')
        c = conn.cursor()
        c.execute('DELETE FROM websites WHERE websiteName = ?', (websiteName,))
        conn.commit()
        conn.close()
