import sqlite3
import datetime
import tkinter as tk

def create_logs_database():
    #Connect to the SQLite database
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()

    #Create a table to store logs if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL
        )
    ''')

    #Commit changes and close the connection
    conn.commit()
    conn.close()

def updateLog(message,logText):
    # Insert the log message into the database
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()

    logText.config(state=tk.NORMAL) #Enable edits

    # Get the time
    current_time = datetime.datetime.now()
    # Remove the displayed microseconds from current_time
    loggedTime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + " " + \
                 str(current_time.hour) + ":" + str(current_time.minute)+ ":" + str(current_time.second) + " "

    logText.insert(tk.END, loggedTime + message + "\n") # Add message to the end of the previous one
    logText.config(state=tk.DISABLED) # Disable edits

    print(loggedTime + message+ '\n') # For debugging
    return logText

def cleanup_old_logs():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    #Delete all log messages older than 2 weeks
    cursor.execute("DELETE FROM logs WHERE timestamp < datetime('now', '-14 days')")
    conn.commit()
    conn.close()

def loadLogs(logsText):
    # Enable editing
    logsText.config(state=tk.NORMAL)
    # Clear the existing logs in the text widget
    logsText.delete(1.0, tk.END)

    # Fetch the logs from the database
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, message FROM logs ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    conn.close()

    # Insert the logs into the text widget
    for log in logs:
        logsText.insert(tk.END, f"{log[0]} - {log[1]}\n")

    # Disable editing
    logsText.config(state=tk.DISABLED)
    return logsText