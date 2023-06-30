from flask import Flask, render_template, jsonify, request, redirect
import datetime
from funcs import *
from sql import *

# commented code is for MAX7219 and DHT11 sensor
# remember to uncomment in funcs.py also

# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.virtual import viewport, sevensegment
# import Adafruit_DHT

app = Flask(__name__)


connect_to_database()
progress_bars = getSQLData()


# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=1)
# seg = sevensegment(device)
# DATA_PIN = 17
# SENSOR_TYPE = Adafruit_DHT.DHT11

## main route with progress bars
@app.route('/')
def index():
    active_progress_bars = []
    inactive_progress_bars = []

    for progress_bar in progress_bars:
        if progress_bar['printingState'] != 0:
            active_progress_bars.append(progress_bar)
        else:
            inactive_progress_bars.append(progress_bar)

    return render_template('index.html', inactive=inactive_progress_bars, progress_bars=active_progress_bars)

@app.route('/home')
def home():
    return render_template('home.html')


## route to add printer to database
@app.route('/add_printer', methods=['GET', 'POST'])
def add_printer():
    if request.method == 'POST':
        model = request.form['model']
        manufacturer = request.form['manufacturer']
        printer_type = request.form['type']
        state = request.form['state']
        insert_printer(model, manufacturer, printer_type, state)
        return 'Printer added successfully!'
    return render_template('add_printer.html')

## route to add filament to database
@app.route('/add_filament', methods=['GET', 'POST'])
def add_filament():
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        color = request.form['color']
        mass = request.form['mass']
        material_type = request.form['material_type']
        insert_filament(manufacturer, color, mass, material_type)
        return 'Filament added successfully!'
    return render_template('add_filament.html')


## route to start a new printing
@app.route('/change_time', methods=['GET','POST'])
def change_time():
    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M')

    ## testing data
    filaments= ['PLA_bialy_1','PLA_bialy_2','PLA_czarny_1','PLA_szary_1',] 

    if request.method == 'POST':

        progress_bar_id = request.form['progress_bar_id']
        filamentID = request.form['filament-id']
        filamentAmount = request.form['material-amount']
        username = request.form['username']

        start_time = datetime.datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        finish_time = datetime.datetime.strptime(request.form['finish_time'], '%Y-%m-%dT%H:%M')

        # Find the progress bar with the given ID and update its start and finish times
        for progress_bar in progress_bars:
            if progress_bar['printerID'] == progress_bar_id:
                progress_bar['filamentID'] = filamentID
                progress_bar['materialAmount'] = filamentAmount
                progress_bar['startTime'] = start_time
                progress_bar['endTime'] = finish_time
                progress_bar['printingState'] = 1
                progress_bar['username'] = username
                currentPrintingUpdate(progress_bar)
                break

        # Redirect back to the index page after updating the times
        return redirect('/')
    return render_template('change_time.html',progress_bars=progress_bars,current_time=currentTime,filaments=filaments)

## route to update progress bars
@app.route('/progress')
def fetch_progress():
    for progress_bar in progress_bars:
        currProgress, additional_info = calculate_progress(progress_bar['startTime'], progress_bar['endTime'])
        progress_bar['progress'] = currProgress
        progress_bar['additional_info'] = additional_info

        ## electronics
        
        # if progress_bar['printerID'] == "Ender3_1":
        #     # humid, temp = getTempHumid(DATA_PIN, SENSOR_TYPE)
        #     # progress_bar['temperature'] = temp
        #     # progress_bar['humidity'] = humid
        #     # seg.text = stringToDisplay(progress_bar)
            
    return jsonify({'progress_bars': progress_bars})

## route to end printing
@app.route('/reset_printer',  methods=['GET','POST'])
def reset_printer():
    printer_id = request.args.get('printer_id')
    for some_progress_bar in progress_bars:
        if some_progress_bar['printerID'] == printer_id:
            progress_bar = some_progress_bar
            break
    
    if request.method == 'POST':
        printer_id = request.form['printer_id']
        materialAmount = request.form['materialAmount']
        checkbox = request.form.get('myCheckbox')
        outcome = "success" if checkbox else "failure"
        for progress_bar in progress_bars:
            if progress_bar['printerID'] == printer_id:
                progress_bar['materialAmount'] = materialAmount
                progress_bar['printingState'] = 0
                add_printingStory(progress_bar,outcome)
                currentPrintingUpdate(progress_bar)
                break
        return redirect('/')
    return render_template('reset_printer.html', printer_id = printer_id, progress_bar = progress_bar)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
