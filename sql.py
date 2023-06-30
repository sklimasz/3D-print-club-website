import sqlite3
import json
import datetime
from funcs import *
from random import randint

def connect_to_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    ## database containing current usage of 3D printers
    cursor.execute('''CREATE TABLE IF NOT EXISTS currentPrinting
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                printerID INTEGER NOT NULL,
                filamentID INTEGER NOT NULL,
                materialAmount INTEGER NOT NULL,
                startTime TEXT NOT NULL,
                endTime TEXT NOT NULL,
                printingState INTEGER NOT NULL,
                username TEXT NOT NULL)''')
    
    ## database containing all printings for analyzing
    cursor.execute('''CREATE TABLE IF NOT EXISTS previousPrinting
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                printerID INTEGER NOT NULL,
                filamentID INTEGER NOT NULL,
                materialAmount INTEGER NOT NULL,
                startTime TEXT NOT NULL,
                endTime TEXT NOT NULL,
                username TEXT NOT NULL,
                outcome TEXT NOT NULL)''')
    
    ## database of printers
    cursor.execute('''CREATE TABLE IF NOT EXISTS printers
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                manufacturer TEXT NOT NULL,
                type TEXT NOT NULL,
                state TEXT NOT NULL)''')
    ## database of filaments
    cursor.execute('''CREATE TABLE IF NOT EXISTS filaments
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                manufacturer TEXT NOT NULL,
                color TEXT NOT NULL,
                mass INTEGER NOT NULL,
                materialType TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()


def get_printingStory(ID):
    ## gets all printing story for given printer
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row  # Enable the Row factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM previousPrinting WHERE ID=?", (ID,))
        row = cursor.fetchone()
        if row:
            return dict(row)  # Convert the row to a dictionary
        return None  # Return None if no row is found

def add_printingStory(progress_bar, outcome):
    ## adds printing to previous printings (when printing finishes)
    copy = progress_bar.copy()
    copy["startTime"] = datetime.datetime.strftime(copy["startTime"], '%Y-%m-%dT%H:%M')
    copy["endTime"] = datetime.datetime.strftime(copy["endTime"], '%Y-%m-%dT%H:%M')
    validKeys = ["printerID", "filamentID", "materialAmount", "startTime","endTime", "username"]

    values = [ copy[key] for key in list(progress_bar.keys()) if key in validKeys ]
    values.append(outcome)
    with sqlite3.connect('database.db') as conn:
        sql_command = """INSERT INTO previousPrinting
        (printerID, filamentID, materialAmount, startTime, endTime, username, outcome)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
        conn.execute(sql_command, tuple(values))
        conn.commit()

def currentPrintingFill(printerID,filamentID):
    ## fills current printings
    ## (used on site initialization and when printer state is changed (e.g repaired)
    for x,y in zip(printerID,filamentID):
        with sqlite3.connect('database.db') as conn:
            dt = datetime.datetime.now()
            dtplus = dt + datetime.timedelta(weeks = 5200)

            dtplus = dtplus.strftime('%Y-%m-%dT%H:%M')
            dt = dt.strftime('%Y-%m-%dT%H:%M')

            conn.execute("""INSERT INTO
                        currentPrinting (printerID, filamentID, materialAmount, startTime, endTime, printingState, username)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (x, y,randint(100,500), dt, dtplus, 0, "none" ))
            conn.commit()

    
def currentPrintingUpdate(progress_bar):
    ## when a printing is started
    copy = progress_bar.copy()
    copy["startTime"] = datetime.datetime.strftime(copy["startTime"], '%Y-%m-%dT%H:%M')
    copy["endTime"] = datetime.datetime.strftime(copy["endTime"], '%Y-%m-%dT%H:%M')
    validKeys = ["printerID", "filamentID", "materialAmount", "startTime", "endTime", "printingState", "username"]

    values = [ copy[key] for key in list(progress_bar.keys()) if key in validKeys ]
    values.append(copy['printerID'])

    with sqlite3.connect('database.db') as conn:
        sql_command = """UPDATE currentPrinting
        SET printerID = ?, filamentID = ?, materialAmount = ?, startTime = ?, endTime = ?, printingState = ?, username = ?
        WHERE printerID = ?"""
        conn.execute(sql_command, tuple(values))
        conn.commit()

def getCurrentPrinting(printerID):
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row  # Enable the Row factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM currentPrinting WHERE printerID = ?", (printerID,))
        row = cursor.fetchone()
        if row:
            row = dict(row)
            row.pop("ID", None)
            return dict(row)  # Convert the row to a dictionary
        return None  # Return None if no row is found
    
def fetch_printersID():
    ## get all current working printers ID
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT printerID FROM currentPrinting")
        rows = cursor.fetchall()
        column_values = [row[0] for row in rows]  # Extract the values from the result rows
        return column_values
    
def insert_printer(model, manufacturer, printer_type, state):
    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO printers (model, manufacturer, type, state) VALUES (?, ?, ?, ?)",
                     (model, manufacturer, printer_type, state))
        conn.commit()

def insert_filament(manufacturer, color, mass, material_type):
    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO filaments (manufacturer, color, mass, materialType) VALUES (?, ?, ?, ?)",
                     (manufacturer, color, mass, material_type))
        conn.commit()
        

if __name__ == "__main__":
    ## used on initialization only
    arr1 = ['Ender3_1','Ender3_2','Dreamer_1','Dreamer_2', 'GuiderII_1']
    arr2 = ['PLA_bialy_1','PLA_bialy_2','PLA_czarny_1','PLA_szary_1',]
    connect_to_database()
    currentPrintingFill(arr1,arr2)

    ### check what was saved
    #print(get_printingStory(1))


