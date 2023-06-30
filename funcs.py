import datetime
from sql import *


## import Adafruit_DHT

def calculate_progress(start_time, finish_time):
    current_time = datetime.datetime.now()
    total_duration = finish_time - start_time
    elapsed_duration = current_time - start_time
    progress = int((elapsed_duration / total_duration) * 100)

    if progress >= 100:
        progress = 100
        additional_info = "Process completed!"
    else:
        additional_info = f"Completed {progress}%"
    return progress, additional_info

def sqlData_to_htmlData(row):
    start_time = datetime.datetime.strptime(row["startTime"], '%Y-%m-%dT%H:%M')
    finish_time = datetime.datetime.strptime(row["endTime"], '%Y-%m-%dT%H:%M')

    progress, additional_info = calculate_progress(start_time, finish_time)
    progressBar = row.copy()
    progressBar['startTime'] = start_time
    progressBar['endTime'] = finish_time
    progressBar['progress'] = progress
    progressBar['additional_info'] = additional_info

    return progressBar

def getSQLData():
    progress_bars = []
    printersID = fetch_printersID()

    for ID in printersID:
        temp = getCurrentPrinting(ID)
        temp = sqlData_to_htmlData(temp)
        progress_bars.append(temp)
        print(temp)
    return progress_bars

def stringToDisplay(progress_bar):
    progress = progress_bar['progress']
    state = progress_bar['printingState']

    if (state == 0):
        toDisplay = "rEAdY"
    elif (progress < 10):
        toDisplay = f"ProG 00{progress}"
    elif (progress < 100):
        toDisplay = f"ProG 0{progress}"
    else:
        toDisplay = "ConPLEtE"
    return toDisplay

# def getTempHumid(DATA_PIN,SENSOR_TYPE):
#     humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, DATA_PIN)

#     return [f'{humidity:.2f}',f'{temperature:.2f}']
